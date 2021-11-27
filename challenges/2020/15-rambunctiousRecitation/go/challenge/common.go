package challenge

import (
	"strconv"
	"strings"
)

func findValueN(instr string, threshold int) int {
	var inp []int
	for _, x := range strings.Split(strings.TrimSpace(instr), ",") {
		i, err := strconv.Atoi(x)
		if err != nil {
			panic(err)
		}
		inp = append(inp, i)
	}

	indexes := make(map[int]int)

	for i, n := range inp {
		indexes[n] = i
	}

	for len(inp) < threshold {
		c := len(inp) - 1
		previousNumber := inp[c]

		var previousOccuranceIndex int
		val, found := indexes[previousNumber]
		if !found {
			previousOccuranceIndex = -1
		} else {
			previousOccuranceIndex = val
		}

		var newNumber int

		if previousOccuranceIndex != -1 {
			newNumber = c - previousOccuranceIndex
		}

		indexes[previousNumber] = c
		inp = append(inp, newNumber)
	}

	return inp[len(inp)-1]
}
