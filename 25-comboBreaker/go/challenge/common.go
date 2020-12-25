package challenge

import (
	"strconv"
	"strings"
)

func parse(instr string) []int {
	var o []int
	for _, x := range strings.Split(strings.TrimSpace(instr), "\n") {
		i, err := strconv.Atoi(x)
		if err != nil {
			panic(err)
		}
		o = append(o, i)
	}
	return o
}
