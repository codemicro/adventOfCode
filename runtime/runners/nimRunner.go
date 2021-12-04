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
)

const nimInstallation = "nim"

type nimRunner struct {
	dir   string
	tasks []*Task
}

func newNimRunner(dir string) Runner {
	return &nimRunner{
		dir: dir,
	}
}

func (n *nimRunner) Queue(task *Task) {
	n.tasks = append(n.tasks, task)
}

//go:embed interface/nim.nim
var nimInterface []byte

func (n *nimRunner) Run() (chan ResultOrError, func()) {

	wrapperExecutable := "runtimeWrapper"
	wrapperFilename := wrapperExecutable + ".nim"

	executableFilepath := filepath.Join(n.dir, wrapperExecutable)
	wrapperFilepath := filepath.Join(n.dir, wrapperFilename)

	// generate interaction data
	taskJSON, err := json.Marshal(n.tasks)
	if err != nil {
		return makeErrorChan(err), nil
	}

	// save interaction code
	err = ioutil.WriteFile(wrapperFilepath, nimInterface, 0644)
	if err != nil {
		return makeErrorChan(err), nil
	}

	fmt.Print("Compiling...\r")
	defer fmt.Print("\n\n")

	// compile
	stderrBuffer := new(bytes.Buffer)
	cmd := exec.Command(nimInstallation, "compile", "-o:"+executableFilepath, "-d:release", wrapperFilepath)
	cmd.Stderr = stderrBuffer
	err = cmd.Run()
	if err != nil {
		return makeErrorChan(fmt.Errorf("compilation failed: %s: %s", err, stderrBuffer.String())), nil
	}

	if !cmd.ProcessState.Success() {
		return makeErrorChan(errors.New("compilation failed, hence cannot continue")), nil
	}

	fmt.Print("Running...         ")

	absExecPath, err := filepath.Abs(executableFilepath)
	if err != nil {
		return makeErrorChan(err), nil
	}

	// run
	cmd = exec.Command(absExecPath)
	cmd.Dir = n.dir
	cmd.Stdin = bytes.NewReader(append(taskJSON, '\n'))

	return readResultsFromCommand(cmd), func() {
		_ = os.Remove(executableFilepath)
		_ = os.Remove(wrapperFilepath)
	}
}
