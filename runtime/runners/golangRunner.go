package runners

import (
	"bytes"
	_ "embed"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"text/template"
)

const golangInstallation = "go"

type golangRunner struct {
	dir string
	tasks []*Task
}

func newGolangRunner(dir string) Runner {
	return &golangRunner{
		dir: dir,
	}
}

func (g *golangRunner) Queue(task *Task) {
	g.tasks = append(g.tasks, task)
}

//go:embed interface/go.go
var golangInterface []byte

func (g *golangRunner) Run() chan ResultOrError {

	wrapperFilename := "runtime-wrapper.go"
	wrapperExecutable := "runtime-wrapper"

	wrapperFilepath := filepath.Join(g.dir, wrapperFilename)
	wrapperExecutableFilepath := filepath.Join(g.dir, wrapperExecutable)

	// generate interaction data
	taskJSON, err := json.Marshal(g.tasks)
	if err != nil {
		return makeErrorChan(err)
	}

	// determine package import path
	buildPath := fmt.Sprintf("github.com/codemicro/adventOfCode/challenges/%s/%s", filepath.Base(filepath.Dir(g.dir)), filepath.Base(g.dir))
	importPath := buildPath + "/go"

	// generate code
	var wrapperContent []byte
	{
		tpl := template.Must(template.New("").Parse(string(golangInterface)))
		b := new(bytes.Buffer)
		err := tpl.Execute(b, struct {
			ImportPath string
		}{importPath})
		if err != nil {
			return makeErrorChan(err)
		}
		wrapperContent = b.Bytes()
	}

	// save interaction code
	err = ioutil.WriteFile(wrapperFilepath, wrapperContent, 0644)
	if err != nil {
		return makeErrorChan(err)
	}

	// compile executable
	stderrBuffer := new(bytes.Buffer)

	cmd := exec.Command(golangInstallation, "build", "-tags", "runtime", "-o", wrapperExecutableFilepath, buildPath)
	cmd.Stderr = stderrBuffer
	err = cmd.Run()
	if err != nil {
		return makeErrorChan(fmt.Errorf("compilation failed: %s: %s", err, stderrBuffer.String()))
	}

	if !cmd.ProcessState.Success() {
		return makeErrorChan(errors.New("compilation failed, hence cannot continue"))
	}

	absExecPath, err := filepath.Abs(wrapperExecutableFilepath)
	if err != nil {
		return makeErrorChan(err)
	}

	// run executable
	cmd = exec.Command(absExecPath)
	cmd.Dir = g.dir

	cmd.Stdin = bytes.NewReader(append(taskJSON, '\n'))

	return readResultsFromCommand(cmd, func() {
		// remove leftover files
		_ = os.Remove(wrapperFilepath)
		_ = os.Remove(wrapperExecutableFilepath)
	})
}