package runners

import (
	"bytes"
	_ "embed"
	"encoding/json"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"text/template"
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
var pythonInterface string

func (p *pythonRunner) Run() chan ResultOrError {

	wrapperFilename := "runtime-wrapper.py"
	wrapperFilepath := filepath.Join(p.dir, wrapperFilename)

	// Generate interaction code
	taskJSON, err := json.Marshal(p.tasks)
	if err != nil {
		return makeErrorChan(err)
	}

	interactionCodeBuffer := new(bytes.Buffer)
	{
		templ := template.Must(template.New("").Parse(pythonInterface))
		err := templ.Execute(interactionCodeBuffer, struct{
			TasksJSON string
		}{string(taskJSON)})
		if err != nil {
			return makeErrorChan(err)
		}
	}

	// Save interaction code
	err = ioutil.WriteFile(wrapperFilepath, interactionCodeBuffer.Bytes(), 0644)
	if err != nil {
		return makeErrorChan(err)
	}

	// Run Python and gather output
	cmd := exec.Command(python3Installation, "-B", wrapperFilename) // -B prevents .pyc files from being written
	cmd.Dir = p.dir

	return readResultsFromCommand(cmd, func() {
		// Remove leftover files
		_ = os.Remove(wrapperFilepath)
	})
}