package challenge

import (
	"strconv"
	"strings"
)

func applyMask(number int, mask string) int {
	mask = strings.ToLower(mask)
	value := numberToBase(number, 2)
	value = zfill(value, len(mask)-len(value))
	var combi string
	for i := 0; i < len(value); i += 1 {
		v := string(value[i])
		m := string(mask[i])

		if m == "x" {
			combi += v
		} else {
			combi += m
		}
	}
	ix, err := strconv.ParseInt(combi, 2, 64)
	if err != nil {
		panic(err)
	}
	return int(ix)
}

func PartOne(instr string) int {
	inputInstructions := parse(instr)
	memory := make(map[int]int)

	for _, instruction := range inputInstructions {
		memory[instruction.Address] = applyMask(instruction.Value, instruction.Mask)
	}

	var sigma int
	for _, v := range memory {
		sigma += v
	}
	return sigma
}
