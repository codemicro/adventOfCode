package runners

import (
	"bytes"
	_ "embed"
	"encoding/json"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
)

const python3Installation = "python3"

type pythonRunner struct {
	dir   string
	tasks []*Task
}

func newPythonRunner(dir string) Runner {
	return &pythonRunner{
		dir: dir,
	}
}

func (p *pythonRunner) Queue(task *Task) {
	p.tasks = append(p.tasks, task)
}

//go:embed interface/python.py
var pythonInterface []byte

func (p *pythonRunner) Run() (chan ResultOrError, func()) {

	wrapperFilename := "runtime-wrapper.py"
	wrapperFilepath := filepath.Join(p.dir, wrapperFilename)

	// Generate interaction data
	taskJSON, err := json.Marshal(p.tasks)
	if err != nil {
		return makeErrorChan(err), nil
	}

	// Save interaction code
	err = ioutil.WriteFile(wrapperFilepath, pythonInterface, 0644)
	if err != nil {
		return makeErrorChan(err), nil
	}

	cwd, err := os.Getwd()
	if err != nil {
		return makeErrorChan(err), nil
	}

	pythonPathVar := filepath.Join(cwd, "lib")

	// Run Python and gather output
	cmd := exec.Command(python3Installation, "-B", wrapperFilename) // -B prevents .pyc files from being written
	cmd.Env = append(cmd.Env, "PYTHONPATH="+pythonPathVar) // this allows the aocpy lib to be imported
	cmd.Dir = p.dir

	cmd.Stdin = bytes.NewReader(append(taskJSON, '\n'))

	return readResultsFromCommand(cmd), func() {
		// Remove leftover files
		_ = os.Remove(wrapperFilepath)
	}
}
