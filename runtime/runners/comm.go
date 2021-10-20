package runners

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os/exec"
	"strings"
	"sync"
)

type Task struct {
	Part      Part   `json:"part"`
	Input     string `json:"input"`
	OutputDir string `json:"output_dir,omitempty"`
}

type Result struct {
	TaskNumber int     `json:"task_n"`
	Ok         bool    `json:"ok"`
	Output     string  `json:"output"`
	Duration   float32 `json:"duration"`
}

func makeErrorChan(err error) chan ResultOrError {
	c := make(chan ResultOrError, 1)
	c <- ResultOrError{Error: err}
	close(c)
	return c
}

// custom writer type

type customWriter struct {
	pending []byte
	entries [][]byte
	mux sync.Mutex
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

func readResultsFromCommand(cmd *exec.Cmd, cleanupFn func()) chan ResultOrError {

	stdoutWriter := &customWriter{}
	stderrBuffer := new(bytes.Buffer)

	cmd.Stdout = stdoutWriter
	cmd.Stderr = stderrBuffer

	err := cmd.Start()
	if err != nil {
		return makeErrorChan(err)
	}

	// Command status listener
	status := make(chan bool) // true if success, false if failure

	go func() {
		_ = cmd.Wait()
		status <- cmd.ProcessState.Success()
		close(status)
	}()

	// Now let's read some results

	c := make(chan ResultOrError)

	go func() {
	readerLoop:
		for {
			inp, err := stdoutWriter.GetEntry()
			// will return an error if there is nothing to retrieve
			if err == nil {

				res := new(Result)
				err = json.Unmarshal(inp, res)
				if err != nil {
					// echo anything that won't parse to stdout (this lets us add debug print statements)
					fmt.Printf("AA %#v\n", strings.TrimSpace(string(inp)))
				} else {
					c <- ResultOrError{Result: res}
				}

			}

			select {
			case successfulFinish := <-status:
				if !successfulFinish {
					c <- ResultOrError{Error: errors.New("run failed: " + stderrBuffer.String())}
				}
				break readerLoop
			default:
			}
		}
		close(c)

		if cleanupFn != nil {
			cleanupFn()
		}
	}()

	return c
}