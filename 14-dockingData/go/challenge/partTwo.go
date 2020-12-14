package challenge

import (
	"strconv"
	"strings"
)

// The following two functions were taken from https://stackoverflow.com/a/19249957
func generateCombinations(alphabet string, length int) <-chan string {
	c := make(chan string)
	go func(c chan string) {
		defer close(c)
		addLetter(c, "", alphabet, length)
	}(c)
	return c
}
func addLetter(c chan string, combo string, alphabet string, length int) {
	if length <= 0 {
		return
	}

	var newCombo string
	for _, ch := range alphabet {
		newCombo = combo + string(ch)
		c <- newCombo
		addLetter(c, newCombo, alphabet, length-1)
	}
}

// end taken functions

func getMemoryAddresses(number int, mask string) []int {
	mask = strings.ToLower(mask)
	value := numberToBase(number, 2)
	value = zfill(value, len(mask)-len(value))

	var combi []string

	for i := 0; i < len(value); i += 1 {
		v := string(value[i])
		m := string(mask[i])

		var av string

		if m == "0" {
			av = v
		} else if m == "1" {
			av = "1"
		} else {
			av = m
		}

		combi = append(combi, av)
	}

	var xns []int

	n := strings.Count(mask, "x")
	for valstring := range generateCombinations("01", n) {
		if len(valstring) != n {
			continue
		}
		val_combo := strings.Split(valstring, "")
		msk := make([]string, len(combi))
		copy(msk, combi)
		var val_counter int
		for i, char := range msk {
			if char == "x" {
				msk[i] = val_combo[val_counter]
				val_counter += 1
			}
		}
		ix, err := strconv.ParseInt(strings.Join(msk, ""), 2, 64)
		if err != nil {
			panic(err)
		}
		xns = append(xns, int(ix))
	}

	return xns
}

func PartTwo(instr string) int {
	inputInstructions := parse(instr)
	memory := make(map[int]int)

	for _, instruction := range inputInstructions {
		addresses := getMemoryAddresses(instruction.Address, instruction.Mask)
		for _, address := range addresses {
			memory[address] = instruction.Value
		}
	}

	var sigma int
	for _, v := range memory {
		sigma += v
	}
	return sigma
}
