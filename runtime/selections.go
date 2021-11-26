package main

import (
	"errors"
	"fmt"
	"github.com/AlecAivazis/survey/v2"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
	"os"
	"path/filepath"
	"strings"
)

func userSelect(question string, choices []string) (int, error) {
	var o string
	prompt := &survey.Select{
		Message: question,
		Options: choices,
	}
	//err := survey.AskOne(prompt, &o, survey.WithStdio(os.Stdin, os.Stderr, os.Stderr))
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

func selectYear(dir string) (string, error) {

	var opts []string

    entries, err := os.ReadDir(dir)
	if err != nil {
        return "", err
    }

	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}
		opts = append(opts, entry.Name())
	}

	if len(opts) == 0 {
		return "", errors.New("no years to use")
	}

	if args.Year != "" {
		for _, x := range opts {
            if x == args.Year {
                fmt.Printf("Selecting year %s\n", args.Year)
				return filepath.Join(dir, x), nil
            }
        }
        fmt.Printf("Could not locate year %s\n", args.Year)
	}

	var selectedYearIndex int

	if x := len(opts); x == 1 {
		selectedYearIndex = 0
		fmt.Printf("Automatically selecting year %s\n", opts[selectedYearIndex])
	} else {
		selectedYearIndex, err = userSelect("Which year do you want to use?", opts)
		if err != nil {
			return "", err
		}
	}

    return filepath.Join(dir, opts[selectedYearIndex]), nil
}

func selectChallenge(dir string) (*challenge.Challenge, error) {

	challenges, err := challenge.ListingFromDir(dir)
	if err != nil {
		return nil, err
	}

	if len(challenges) == 0 {
		return nil, errors.New("no challenges to run")
	}

	if args.ChallengeDay != nil {
		for _, ch := range challenges {
			if ch.Number == *args.ChallengeDay {
				fmt.Printf("Selecting day %d (%s)\n", ch.Number, ch.Name)
				return ch, nil
			}
		}
		fmt.Printf("Could not locate day %d\n", *args.ChallengeDay)
	}

	var selectedChallengeIndex int

	if x := len(challenges); x == 1 {
		selectedChallengeIndex = 0
		c := challenges[0]
		fmt.Printf("Automatically selecting day %d (%s)\n", c.Number, c.Name)
	} else {
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

	if len(implementations) == 0 {
		return "", errors.New("no implementations to use")
	}

	if args.Implementation != "" {
		for _, im := range implementations {
			if strings.EqualFold(im, args.Implementation) {
				fmt.Printf("Selecting %s implementation\n", runners.RunnerNames[im])
				return im, nil
			}
		}
		fmt.Printf("Could not locate implementation %#v\n", args.Implementation)
	}

	var selectedImplementationIndex int

	if x := len(implementations); x == 1 {
		selectedImplementationIndex = 0
		fmt.Printf("Automatically selecting %s implementation", runners.RunnerNames[implementations[0]])
	} else {
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
