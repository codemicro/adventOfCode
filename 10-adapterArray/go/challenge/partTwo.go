package challenge

import (
	"sort"
	"strconv"
	"strings"
)

func PartTwo(instr string) int {
	var joltages []int
	for _, x := range strings.Split(strings.TrimSpace(instr), "\n") {
		i, err := strconv.Atoi(x)
		if err != nil {
			panic(err)
		}
		joltages = append(joltages, i)
	}
	sort.Ints(joltages)

	routeLengths := map[int]int{0: 1}

	for _, joltage := range joltages {
		var totalRoutes int
		for _, n := range []int{1, 2, 3} {
			v, exists := routeLengths[joltage-n]
			if !exists {
				v = 0
			}
			totalRoutes += v
		}
		routeLengths[joltage] = totalRoutes
	}

	return routeLengths[joltages[len(joltages)-1]]
}
