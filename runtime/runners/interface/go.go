//+build runtime

package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"github.com/codemicro/adventOfCode/runtime/runners"
	"os"
	"time"
	chcode "{{ .ImportPath }}"
)

func sendResult(taskID string, ok bool, output string, duration float64) {
	x := runners.Result{
		TaskID:   taskID,
		Ok:       ok,
		Output:   output,
		Duration: duration,
	}
	dat, err := json.Marshal(&x)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(dat))
}

func run() error {
	reader := bufio.NewReader(os.Stdin)
	tasksBytes, err := reader.ReadBytes('\n')
	if err != nil {
		return err
	}

	var tasks []*runners.Task
	if err := json.Unmarshal(tasksBytes, &tasks); err != nil {
		return err
	}

	for _, task := range tasks {
		var run func() (interface{}, error)

		switch task.Part {
		case runners.PartOne:
			run = func() (interface{}, error) {
				return (chcode.Challenge{}).One(task.Input)
			}
		case runners.PartTwo:
			run = func() (interface{}, error) {
				return (chcode.Challenge{}).Two(task.Input)
			}
		case runners.Visualise:
			run = func() (interface{}, error) {
				return "", (chcode.Challenge{}).Vis(task.Input, task.OutputDir)
			}
		}

		startTime := time.Now()
		res, err := run()
		endTIme := time.Now()

		runningTime := endTIme.Sub(startTime).Seconds()

		if err != nil {
			sendResult(task.TaskID, false, err.Error(), runningTime)
		} else {
			sendResult(task.TaskID, true, fmt.Sprintf("%v", res), runningTime)
		}

	}

	return nil

}

func main() {
	if err := run(); err != nil {
		panic(err)
	}
}
