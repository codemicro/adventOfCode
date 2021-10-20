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
	dir string
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

func (p *pythonRunner) Run() chan ResultOrError {

	wrapperFilename := "runtime-wrapper.py"
	wrapperFilepath := filepath.Join(p.dir, wrapperFilename)

	// Generate interaction data
	taskJSON, err := json.Marshal(p.tasks)
	if err != nil {
		return makeErrorChan(err)
	}

	// Save interaction code
	err = ioutil.WriteFile(wrapperFilepath, pythonInterface, 0644)
	if err != nil {
		return makeErrorChan(err)
	}

	// Run Python and gather output
	cmd := exec.Command(python3Installation, "-B", wrapperFilename) // -B prevents .pyc files from being written
	cmd.Dir = p.dir

	cmd.Stdin = bytes.NewReader(append(taskJSON, '\n'))

	return readResultsFromCommand(cmd, func() {
		// Remove leftover files
		_ = os.Remove(wrapperFilepath)
	})
}