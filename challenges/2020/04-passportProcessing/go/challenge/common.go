package challenge

import "strings"

func parse(instr string) []string {
	inputSlice := strings.Split(strings.TrimSpace(instr), "\n\n")
	for i, x := range inputSlice {
		inputSlice[i] = strings.ReplaceAll(x, "\n", " ")
	}
	return inputSlice
}
