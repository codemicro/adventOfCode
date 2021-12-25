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
)

const (
	nimInstallation              = "nim"
	nimWrapperFilename           = "runtimeWrapper.nim"
	nimWrapperExecutableFilename = "runtimeWrapper"
)

type nimRunner struct {
	dir                string
	cmd                *exec.Cmd
	wrapperFilepath    string
	executableFilepath string
	stdin              io.WriteCloser
}

func newNimRunner(dir string) Runner {
	return &nimRunner{
		dir: dir,
	}
}

//go:embed interface/nim.nim
var nimInterface []byte

func (n *nimRunner) Start() error {
	n.wrapperFilepath = filepath.Join(n.dir, nimWrapperFilename)
	n.executableFilepath = filepath.Join(n.dir, nimWrapperExecutableFilename)

	// save interaction code
	err := ioutil.WriteFile(n.wrapperFilepath, nimInterface, 0644)
	if err != nil {
		return err
	}

	// compile
	stderrBuffer := new(bytes.Buffer)
	cmd := exec.Command(nimInstallation, "compile", "-o:"+n.executableFilepath, "-d:release", n.wrapperFilepath)
	cmd.Stderr = stderrBuffer
	err = cmd.Run()
	if err != nil {
		return fmt.Errorf("compilation failed: %s: %s", err, stderrBuffer.String())
	}

	if !cmd.ProcessState.Success() {
		return errors.New("compilation failed, hence cannot continue")
	}

	// now we run!
	absExecPath, err := filepath.Abs(n.executableFilepath)
	if err != nil {
		return err
	}

	n.cmd = exec.Command(absExecPath)
	n.cmd.Dir = n.dir

	if stdin, err := setupBuffers(n.cmd); err != nil {
		return err
	} else {
		n.stdin = stdin
	}

	return n.cmd.Start()
}

func (n *nimRunner) Stop() error {
	if n.cmd == nil || n.cmd.Process == nil {
		return nil
	}
	return n.cmd.Process.Kill()
}

func (n *nimRunner) Cleanup() error {
	if n.wrapperFilepath != "" {
		_ = os.Remove(n.wrapperFilepath)
	}
	if n.executableFilepath != "" {
		_ = os.Remove(n.executableFilepath)
	}
	return nil
}

func (n *nimRunner) Run(task *Task) (*Result, error) {
	taskJSON, err := json.Marshal(task)
	if err != nil {
		return nil, err
	}
	_, _ = n.stdin.Write(append(taskJSON, '\n'))

	res := new(Result)
	if err := readJSONFromCommand(res, n.cmd); err != nil {
		return nil, err
	}
	return res, nil
}
