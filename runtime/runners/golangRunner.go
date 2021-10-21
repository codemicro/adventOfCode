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
	buildPath := fmt.Sprintf("github.com/codemicro/adventOfCode/challenges/%s", filepath.Base(g.dir))
	importPath := buildPath + "/go"

	// generate code
	var wrapperContent []byte
	{
		tpl := template.Must(template.New("").Parse(string(golangInterface)))
		b := bytes.NewBuffer(wrapperContent)
		err := tpl.Execute(b, struct {
			ImportPath string
		}{importPath})
		if err != nil {
			return makeErrorChan(err)
		}
	}

	// save interaction code
	err = ioutil.WriteFile(wrapperFilepath, wrapperContent, 0644)
	if err != nil {
		return makeErrorChan(err)
	}

	// compile executable
	cmd := exec.Command(golangInstallation, "build", "-O", wrapperExecutableFilepath, buildPath)
	err = cmd.Run()
	if err != nil {
		return makeErrorChan(err)
	}

	if !cmd.ProcessState.Success() {
		return makeErrorChan(errors.New("compilation failed, hence cannot continue"))
	}

	// run executable
	cmd = exec.Command(wrapperExecutableFilepath)
	cmd.Dir = g.dir

	cmd.Stdin = bytes.NewReader(append(taskJSON, '\n'))

	return readResultsFromCommand(cmd, func() {
		// remove leftover files
		_ = os.Remove(wrapperFilepath)
		_ = os.Remove(wrapperExecutableFilepath)
	})
}