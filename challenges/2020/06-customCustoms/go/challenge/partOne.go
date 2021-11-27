package challenge

import "strings"

func PartOne(instr string) int {
	newGroup := func(instr string) Group {
		g := Group{}

		individualPax := strings.Split(instr, "\n")
		g.NumPax = len(individualPax)

		for _, pax := range individualPax {
			for _, char := range pax {
				if !IsRuneInSlice(char, g.Questions) {
					g.Questions = append(g.Questions, char)
				}
			}
		}

		return g
	}

	var questionTotal int

	for _, x := range parse(instr) {
		questionTotal += len(newGroup(x).Questions)
	}

	return questionTotal
}
