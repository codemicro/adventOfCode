package main

import (
	"fmt"

	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
	au "github.com/logrusorgru/aurora"
)

type taskLookupTable map[string]func(*runners.Result)

var (
	passLabel       = au.BrightGreen("pass").String()
	failLabel       = au.BrightRed("fail").String()
	incompleteLabel = au.BgBrightRed("did not complete").String()
)

func setupTestTasks(info *challenge.Info, runner runners.Runner, table *taskLookupTable) {

	st := func(part runners.Part, testCases []*challenge.TestCase, runner runners.Runner, table *taskLookupTable) {
		for i, testCase := range testCases {

			// loop variables change, remember? :P
			i := i
			testCase := testCase

			id := fmt.Sprintf("test.%d.%d", part, i)
			runner.Queue(&runners.Task{
				TaskID: id,
				Part:   part,
				Input:  testCase.Input,
			})

			(*table)[id] = func(r *runners.Result) {

				passed := r.Output == testCase.Expected

				fmt.Print(au.Bold(fmt.Sprintf("Test %s: ",
					au.BrightBlue(fmt.Sprintf("%d.%d", part, i)),
				)))

				var status string
				var followUpText string
				if !r.Ok {
					status = incompleteLabel
					followUpText = "saying \"" + r.Output + "\""
				} else if passed {
					status = passLabel
				} else {
					status = failLabel
				}

				if followUpText == "" {
					followUpText = fmt.Sprintf("in %.4f seconds", r.Duration)
				}

				fmt.Print(status)
				fmt.Println(au.Gray(10, " "+followUpText))

				if !passed && r.Ok {
					fmt.Printf(" └ Expected %s, got %s\n", au.BrightBlue(testCase.Expected), au.BrightBlue(r.Output))
				}
			}
		}
	}

	st(runners.PartOne, info.TestCases.One, runner, table)
	st(runners.PartTwo, info.TestCases.Two, runner, table)
}

func setupMainTasks(input string, runner runners.Runner, table *taskLookupTable) {

	for part := runners.PartOne; part <= runners.PartTwo; part += 1 {

		part := part // loop variables need to be copied be used elsewhere to be used in function below, otherwise they
		// become rather wrong

		id := fmt.Sprintf("main.%d", part)
		runner.Queue(&runners.Task{
			TaskID: id,
			Part:   part,
			Input:  input,
		})

		(*table)[id] = func(r *runners.Result) {

			fmt.Print(au.Bold(fmt.Sprintf("Part %d: ", au.Yellow(part))))

			if !r.Ok {
				fmt.Print(incompleteLabel)
				fmt.Println(au.Gray(10, " saying \""+r.Output+"\""))
			} else {
				fmt.Print(au.BrightBlue(r.Output))
				fmt.Println(au.Gray(10, fmt.Sprintf(" in %.4f seconds", r.Duration)))
			}

		}
	}

}
