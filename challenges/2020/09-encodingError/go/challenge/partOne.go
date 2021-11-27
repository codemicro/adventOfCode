package challenge

import (
	"sort"
)

func PartOne(instr string) int {
	inputSlice := parse(instr)

	preambleLen := 25
	if len(inputSlice) < 30 { // This is for test inputs
		preambleLen = 5
	}

	pointer := preambleLen
	for pointer < len(inputSlice) {
		if !hasCombinations(inputSlice[pointer-preambleLen:pointer], inputSlice[pointer]) {
			return inputSlice[pointer]
		}
		pointer += 1
	}

	return 0
}

func hasCombinations(options []int, target int) bool {

	// Remove duplicate options
	{
		keys := make(map[int]bool)
		var new []int

		for _, entry := range options {
			if _, value := keys[entry]; !value {
				keys[entry] = true
				new = append(new, entry)
			}
		}

		options = new
	}

	sort.Ints(options) // sorts in place

	var lPtr int
	rPtr := len(options) - 1

	for lPtr < rPtr {
		v := options[lPtr] + options[rPtr]
		if v == target {
			return true
		} else if v < target {
			lPtr += 1
		} else {
			rPtr -= 1
		}
	}

	return false
}
