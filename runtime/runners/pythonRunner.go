package runners

import (
	_ "embed"
	"encoding/json"
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

const (
	python3Installation   = "python3"
	pythonWrapperFilename = "runtime-wrapper.py"
)

type pythonRunner struct {
	dir             string
	cmd             *exec.Cmd
	wrapperFilepath string
	stdin           io.WriteCloser
}

func newPythonRunner(dir string) Runner {
	return &pythonRunner{
		dir: dir,
	}
}

//go:embed interface/python.py
var pythonInterface []byte

func (p *pythonRunner) Start() error {
	p.wrapperFilepath = filepath.Join(p.dir, pythonWrapperFilename)

	// Save interaction code
	if err := ioutil.WriteFile(p.wrapperFilepath, pythonInterface, 0644); err != nil {
		return err
	}

	// Sort out PYTHONPATH
	cwd, err := os.Getwd()
	if err != nil {
		return err
	}

	absDir, err := filepath.Abs(p.dir)
	if err != nil {
		return err
	}

	pythonPathVar := strings.Join([]string{
		filepath.Join(cwd, "lib"),   // so we can use aocpy
		filepath.Join(absDir, "py"), // so we can import stuff in the challenge directory
	}, ":")

	p.cmd = exec.Command(python3Installation, "-B", pythonWrapperFilename) // -B prevents .pyc files from being written
	p.cmd.Env = append(p.cmd.Env, "PYTHONPATH="+pythonPathVar)
	p.cmd.Dir = p.dir

	if stdin, err := setupBuffers(p.cmd); err != nil {
		return err
	} else {
		p.stdin = stdin
	}

	return p.cmd.Start()
}

func (p *pythonRunner) Stop() error {
	if p.cmd == nil || p.cmd.Process == nil {
		return nil
	}
	return p.cmd.Process.Kill()
}

func (p *pythonRunner) Cleanup() error {
	if p.wrapperFilepath == "" {
		return nil
	}
	_ = os.Remove(p.wrapperFilepath)
	return nil
}

func (p *pythonRunner) Run(task *Task) (*Result, error) {
	taskJSON, err := json.Marshal(task)
	if err != nil {
		return nil, err
	}
	_, _ = p.stdin.Write(append(taskJSON, '\n'))

	res := new(Result)
	if err := readJSONFromCommand(res, p.cmd); err != nil {
		return nil, err
	}
	return res, nil
}
