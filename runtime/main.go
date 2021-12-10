package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"

	"github.com/alexflint/go-arg"
	"github.com/codemicro/adventOfCode/runtime/benchmark"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
	au "github.com/logrusorgru/aurora"
)

const (
	challengeDir      = "challenges"
	challengeInfoFile = "info.json"
)

var args struct {
	Year           string `arg:"-y,--year" help:"AoC year to use"`
	ChallengeDay   *int   `arg:"-d,--day" help:"challenge day number to run"`
	Implementation string `arg:"-i,--implementation" help:"implementation to use"`
	Benchmark      bool   `arg:"-b,--benchmark" help:"benchmark a day's implementations'"`
	BenchmarkN     int    `arg:"-n,--benchmark-n" help:"Number of iterations to run for benchmarking" default:"1000"`
	TestOnly       bool   `arg:"-t,--test-only" help:"Only run test inputs"`
	Visualise      bool   `arg:"-g,--visualise" help:"Run visualisation generation"`
}

func run() error {

	arg.MustParse(&args)

	// List and select year
	selectedYear, err := selectYear(challengeDir)
	if err != nil {
		return err
	}

	// List and select challenges
	selectedChallenge, err := selectChallenge(selectedYear)
	if err != nil {
		return err
	}

	// Load info.json file
	challengeInfo, err := challenge.LoadChallengeInfo(filepath.Join(selectedChallenge.Dir, challengeInfoFile))
	if err != nil {
		return err
	}

	// Load challenge input
	challengeInput, err := ioutil.ReadFile(filepath.Join(selectedChallenge.Dir, challengeInfo.InputFile))
	if err != nil {
		return err
	}
	challengeInputString := string(challengeInput)

	if args.Benchmark {
		return benchmark.Run(selectedChallenge, challengeInputString, args.BenchmarkN)
	}

	// List and select implementations
	selectedImplementation, err := selectImplementation(selectedChallenge)
	if err != nil {
		return err
	}

	runner := runners.Available[selectedImplementation](selectedChallenge.Dir)

	lookupTable := make(taskLookupTable)

	if args.Visualise {
		id := "vis"
		runner.Queue(&runners.Task{
			TaskID:    id,
			Part:      runners.Visualise,
			Input:     challengeInputString,
			OutputDir: ".", // directory the runner is run in, which is the challenge directory
		})

		lookupTable[id] = func(r *runners.Result) {

			fmt.Print(au.Bold("Visualisation: "))

			var status string
			var followUpText string
			if !r.Ok {
				status = incompleteLabel
				followUpText = "saying \"" + r.Output + "\""
			} else {
				status = passLabel
			}

			if followUpText == "" {
				followUpText = fmt.Sprintf("in %.4f seconds", r.Duration)
			}

			fmt.Print(status)
			fmt.Println(au.Gray(10, " "+followUpText))
		}

	} else {
		setupTestTasks(challengeInfo, runner, &lookupTable)
		if !args.TestOnly {
			setupMainTasks(challengeInputString, runner, &lookupTable)
		}
	}

	fmt.Println()

	r, cleanupFn := runner.Run()
	for roe := range r {
		if roe.Error != nil {
			return roe.Error
		}
		// fmt.Println(*roe.Result)
		lookupTable[roe.Result.TaskID](roe.Result)
	}

	if cleanupFn != nil {
		cleanupFn()
	}

	return nil
}

func main() {
	if err := run(); err != nil {
		panic(err)
	}
}
