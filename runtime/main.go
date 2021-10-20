package main

import (
	"fmt"
	"github.com/AlecAivazis/survey/v2"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
	"io/ioutil"
	"path/filepath"
)

const (
	challengeDir      = "challenges"
	challengeInfoFile = "info.json"
)

func userSelect(question string, choices []string) (int, error) {
	var o string
	prompt := &survey.Select{
		Message: question,
		Options: choices,
	}
	err := survey.AskOne(prompt, &o)
	if err != nil {
		return 0, err
	}

	for i, x := range choices {
		if x == o {
			return i, nil
		}
	}

	return -1, nil
}

func run() error {

	// List and select challenges

	challenges, err := challenge.ListingFromDir(challengeDir)
	if err != nil {
		return err
	}

	var selectedChallengeIndex int
	{
		var opts []string
		for _, c := range challenges {
			opts = append(opts, c.String())
		}

		chosen, err := userSelect("Which challenge do you want to run?", opts)
		if err != nil {
			return err
		}

		selectedChallengeIndex = chosen
	}
	selectedChallenge := challenges[selectedChallengeIndex]

	// List and select implementations

	implementations, err := selectedChallenge.GetImplementations()
	if err != nil {
		return err
	}

	var selectedImplementationIndex int
	{
		var opts []string
		for _, i := range implementations {
			opts = append(opts, runners.RunnerNames[i])
		}

		chosen, err := userSelect("Which implementation do you want to use?", opts)
		if err != nil {
			return err
		}

		selectedImplementationIndex = chosen
	}
	selectedImplementation := implementations[selectedImplementationIndex]

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

	for roe := range runner.Run() {
		if roe.Error != nil {
			return roe.Error
		}
		// fmt.Println(*roe.Result)
		lookupTable[roe.Result.TaskID](roe.Result)
	}

	return nil
}

func main() {
	if err := run(); err != nil {
		panic(err)
	}
}
