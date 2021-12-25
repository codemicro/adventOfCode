package runners

import (
	"bytes"
	_ "embed"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"text/template"
)

const (
	golangInstallation              = "go"
	golangWrapperFilename           = "runtime-wrapper.go"
	golangWrapperExecutableFilename = "runtime-wrapper"
)

type golangRunner struct {
	dir                string
	cmd                *exec.Cmd
	wrapperFilepath    string
	executableFilepath string
	stdin              io.WriteCloser
}

func newGolangRunner(dir string) Runner {
	return &golangRunner{
		dir: dir,
	}
}

//go:embed interface/go.go
var golangInterface []byte

func (g *golangRunner) Start() error {
	g.wrapperFilepath = filepath.Join(g.dir, golangWrapperFilename)
	g.executableFilepath = filepath.Join(g.dir, golangWrapperExecutableFilename)

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
			return err
		}
		wrapperContent = b.Bytes()
	}

	// save interaction code
	if err := ioutil.WriteFile(g.wrapperFilepath, wrapperContent, 0644); err != nil {
		return err
	}

	// compile executable
	stderrBuffer := new(bytes.Buffer)

	cmd := exec.Command(golangInstallation, "build", "-tags", "runtime", "-o", g.executableFilepath, buildPath)
	cmd.Stderr = stderrBuffer
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("compilation failed: %s: %s", err, stderrBuffer.String())
	}

	if !cmd.ProcessState.Success() {
		return errors.New("compilation failed, hence cannot continue")
	}

	// now we run!
	absExecPath, err := filepath.Abs(g.executableFilepath)
	if err != nil {
		return err
	}

	// run executable
	g.cmd = exec.Command(absExecPath)
	cmd.Dir = g.dir

	if stdin, err := setupBuffers(g.cmd); err != nil {
		return err
	} else {
		g.stdin = stdin
	}

	return g.cmd.Start()
}

func (g *golangRunner) Stop() error {
	if g.cmd == nil || g.cmd.Process == nil {
		return nil
	}
	return g.cmd.Process.Kill()
}

func (g *golangRunner) Cleanup() error {
	if g.wrapperFilepath != "" {
		_ = os.Remove(g.wrapperFilepath)
	}
	if g.executableFilepath != "" {
		_ = os.Remove(g.executableFilepath)
	}
	return nil
}

func (g *golangRunner) Run(task *Task) (*Result, error) {
	taskJSON, err := json.Marshal(task)
	if err != nil {
		return nil, err
	}
	_, _ = g.stdin.Write(append(taskJSON, '\n'))

	res := new(Result)
	if err := readJSONFromCommand(res, g.cmd); err != nil {
		return nil, err
	}
	return res, nil
}
