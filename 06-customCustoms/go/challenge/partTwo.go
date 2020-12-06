package challenge

import "strings"

func PartTwo(instr string) int {

	checkChar := func(aq map[int][]rune, char rune) (isInAll bool) {

		isInAll = true
		for _, val := range aq {
			if !IsRuneInSlice(char, val) {
				isInAll = false
				break
			}
		}

		return
	}

	newGroup := func(instr string) Group {
		g := Group{}

		individualPax := strings.Split(instr, "\n")
		g.NumPax = len(individualPax)

		paxQuestions := make(map[int][]rune)
		for i, pax := range individualPax {
			paxQuestions[i] = []rune(pax)
		}

		for _, val := range paxQuestions {
			for _, char := range val {
				if checkChar(paxQuestions, char) {
					if !IsRuneInSlice(char, g.Questions) {
						g.Questions = append(g.Questions, char)
					}
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
