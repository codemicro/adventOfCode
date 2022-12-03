package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"strings"

	"github.com/codemicro/adventOfCode/runtime/benchmark"
	au "github.com/logrusorgru/aurora"

	"github.com/alexflint/go-arg"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
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

	fmt.Print(
		au.Bold(
			fmt.Sprintf(
				"%s-%d %s (%s)\n\n",
				strings.TrimPrefix(selectedYear, "challenges/"),
				selectedChallenge.Number,
				selectedChallenge.Name,
				runners.RunnerNames[selectedImplementation],
			),
		),
	)

	runner := runners.Available[selectedImplementation](selectedChallenge.Dir)
	if err := runner.Start(); err != nil {
		return err
	}
	defer func() {
		_ = runner.Stop()
		_ = runner.Cleanup()
	}()

	if args.Visualise {
		id := "vis"
		r, err := runner.Run(&runners.Task{
			TaskID:    id,
			Part:      runners.Visualise,
			Input:     challengeInputString,
			OutputDir: ".", // directory the runner is run in, which is the challenge directory
		})
		if err != nil {
			return err
		}

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

	} else {

		if err := runTests(runner, challengeInfo); err != nil {
			return err
		}

		if !args.TestOnly {
			if err := runMainTasks(runner, challengeInputString); err != nil {
				return err
			}
		}
	}

	return nil
}

func main() {
	if err := run(); err != nil {
		panic(err)
	}
}
