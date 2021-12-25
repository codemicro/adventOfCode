package runners

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"os/exec"
	"sync"
	"time"
)

type Task struct {
	TaskID    string `json:"task_id"`
	Part      Part   `json:"part"`
	Input     string `json:"input"`
	OutputDir string `json:"output_dir,omitempty"`
}

type Result struct {
	TaskID   string  `json:"task_id"`
	Ok       bool    `json:"ok"`
	Output   string  `json:"output"`
	Duration float64 `json:"duration"`
}

func makeErrorChan(err error) chan ResultOrError {
	c := make(chan ResultOrError, 1)
	c <- ResultOrError{Error: err}
	close(c)
	return c
}

type customWriter struct {
	pending []byte
	entries [][]byte
	mux     sync.Mutex
}

func (c *customWriter) Write(b []byte) (int, error) {
	var n int

	c.mux.Lock()
	for _, x := range b {
		if x == '\n' {
			c.entries = append(c.entries, c.pending)
			c.pending = nil
		} else {
			c.pending = append(c.pending, x)
		}
		n += 1
	}
	c.mux.Unlock()

	return n, nil
}

func (c *customWriter) GetEntry() ([]byte, error) {
	c.mux.Lock()
	defer c.mux.Unlock()
	if len(c.entries) == 0 {
		return nil, errors.New("no entries")
	}
	var x []byte
	x, c.entries = c.entries[0], c.entries[1:]
	return x, nil
}

func setupBuffers(cmd *exec.Cmd) (io.WriteCloser, error) {
	stdoutWriter := &customWriter{}
	cmd.Stdout = stdoutWriter
	cmd.Stderr = new(bytes.Buffer)
	return cmd.StdinPipe()
}

func checkWait(cmd *exec.Cmd) ([]byte, error) {
	c := cmd.Stdout.(*customWriter)
	for {
		e, err := c.GetEntry()
		if err == nil {
			return e, nil
		}
		
		if cmd.ProcessState != nil {
			// this is only populated after program exit - we have an issue
			return nil, fmt.Errorf("run failed with exit code %d: %s", cmd.ProcessState.ExitCode(), cmd.Stderr.(*bytes.Buffer).String())
		}

		time.Sleep(time.Millisecond * 10)
	}
}
