package main

import (
	"errors"
	"fmt"
	"github.com/AlecAivazis/survey/v2"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
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

func selectChallenge(dir string) (*challenge.Challenge, error) {

	challenges, err := challenge.ListingFromDir(dir)
	if err != nil {
		return nil, err
	}

	var selectedChallengeIndex int

	switch len(challenges) {
	case 0:
		return nil, errors.New("no challenges to run")
	case 1:
		selectedChallengeIndex = 0
		c := challenges[0]
		fmt.Printf("Automatically selecting day %d (%s)\n", c.Number, c.Name)
	default:
		var opts []string
		for _, c := range challenges {
			opts = append(opts, c.String())
		}

		selectedChallengeIndex, err = userSelect("Which challenge do you want to run?", opts)
		if err != nil {
			return nil, err
		}
	}

	return challenges[selectedChallengeIndex], nil
}

func selectImplementation(ch *challenge.Challenge) (string, error) {

	implementations, err := ch.GetImplementations()
	if err != nil {
		return "", err
	}

	var selectedImplementationIndex int

	switch len(implementations) {
	case 0:
		return "", errors.New("no implementations to use")
	case 1:
		selectedImplementationIndex = 0
		fmt.Printf("Automatically selecting implementation %s", runners.RunnerNames[implementations[0]])
	default:
		var opts []string
		for _, i := range implementations {
			opts = append(opts, runners.RunnerNames[i])
		}

		selectedImplementationIndex, err = userSelect("Which implementation do you want to use?", opts)
		if err != nil {
			return "", err
		}
	}

	return implementations[selectedImplementationIndex], nil
}
