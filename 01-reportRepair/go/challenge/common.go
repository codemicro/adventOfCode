package challenge

import (
	"strconv"
	"strings"
)

func parse(instr string) []int {
	inputSlice := strings.Split(strings.TrimSpace(instr), "\n")

	var values []int
	for _, v := range inputSlice {
		str, _ := strconv.Atoi(v)
		values = append(values, str)
	}

	return values
}
