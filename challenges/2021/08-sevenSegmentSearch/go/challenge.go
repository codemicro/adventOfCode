package challenge

import (
	"errors"
	"sort"
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

var (
	digits = []string{
		"abcefg",
		"cf",
		"acdeg",
		"acdfg",
		"bcdf",
		"abdfg",
		"abdefg",
		"acf",
		"abcdefg",
		"abcdfg",
	}
	possibleWirings = aocgo.StringPermutations("abcdefg")
)

type Display struct {
	samples []string
	outputs []string
}

func sortString(s string) string {
	x := []rune(s)
	sort.Slice(x, func(i, j int) bool {
		return x[i] < x[j]
	})
	return string(x)
}

func parse(instr string) []*Display {
	var o []*Display
	for _, line := range strings.Split(strings.TrimSpace(instr), "\n") {
		sp := strings.Split(line, " | ")
		rawSampleString := sp[0]
		rawOutputString := sp[1]

		var samples []string
		for _, x := range strings.Split(rawSampleString, " ") {
			samples = append(samples, sortString(x))
		}

		var outputs []string
		for _, x := range strings.Split(rawOutputString, " ") {
			outputs = append(outputs, sortString(x))
		}

		o = append(o, &Display{
			samples: samples,
			outputs: outputs,
		})
	}
	return o
}

func isDigitValid(digit string) bool {
	for _, d := range digits {
		if digit == d {
			return true
		}
	}
	return false
}

func translateDigit(mapping, inputDigit string) string {
	var o string
	for _, char := range inputDigit {
		n := rune(char) - 'a'
		o += string(mapping[n])
	}
	return sortString(o)
}

func isWiringValid(samples []string, wiring string) bool {
	for _, sample := range samples {
		if !isDigitValid(translateDigit(wiring, sample)) {
			return false
		}
	}
	return true
}

func findValidWiringFromSamples(samples []string) (string, error) {
	for _, wiring := range possibleWirings {
		if isWiringValid(samples, wiring) {
			return wiring, nil
		}
	}
	return "", errors.New("no valid wiring")
}

func getDisplayOutput(display *Display) (int, error) {
	validWiring, err := findValidWiringFromSamples(display.samples)
	if err != nil {
		return 0, err
	}
	var o int
	for _, digit := range display.outputs {
		o *= 10
		translated := translateDigit(validWiring, digit)
		for i, y := range digits {
			if translated == y {
				o += i
				break
			}
		}
	}
	return o, nil
}

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	displays := parse(instr)
	var sigma int
	for _, display := range displays {
		for _, digit := range display.outputs {
			ld := len(digit)
			if ld == len(digits[1]) || ld == len(digits[4]) || ld == len(digits[7]) ||ld == len(digits[8]) {
				sigma += 1
			}
		}
	}
	return sigma, nil
}

func (c Challenge) Two(instr string) (interface{}, error) {
	displays := parse(instr)
	var sigma int
	for _, display := range displays {
		s, err := getDisplayOutput(display)
		if err != nil {
			return nil, err
		}
		sigma += s
	}
	return sigma, nil
}
