package main

import (
	"fmt"
	"github.com/alexflint/go-arg"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
	"io/ioutil"
	"path/filepath"
)

const (
	challengeDir      = "challenges"
	challengeInfoFile = "info.json"
)

var args struct {
	Year           string `arg:"-y,--year" help:"AoC year to use"`
	ChallengeDay   *int   `arg:"-d,--day" help:"challenge day number to run"`
	Implementation string `arg:"-i,--implementation" help:"implementation to use"`
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

	// List and select implementations
	selectedImplementation, err := selectImplementation(selectedChallenge)
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

	runner := runners.Available[selectedImplementation](selectedChallenge.Dir)

	lookupTable := make(taskLookupTable)
	setupTestTasks(challengeInfo, runner, &lookupTable)
	setupMainTasks(challengeInputString, runner, &lookupTable)

	fmt.Println("\nRunning...\n")

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
