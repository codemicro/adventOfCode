package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"

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
		//return benchmark.Run(selectedChallenge, challengeInputString, args.BenchmarkN)
	}

	// List and select implementations
	selectedImplementation, err := selectImplementation(selectedChallenge)
	if err != nil {
		return err
	}

	fmt.Println()

	runner := runners.Available[selectedImplementation](selectedChallenge.Dir)
	if err := runner.Start(); err != nil {
		return err
	}
	defer func() {
		_ = runner.Stop()
		_ = runner.Cleanup()
	}()


	if err := runTests(runner, challengeInfo); err != nil {
		return err
	}

	if err := runMainTasks(runner, challengeInputString); err != nil {
		return err
	}

	return nil
}

func main() {
	if err := run(); err != nil {
		panic(err)
	}
}
