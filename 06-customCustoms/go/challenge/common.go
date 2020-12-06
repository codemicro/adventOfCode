package challenge

import "strings"

func parse(instr string) []string {
	return strings.Split(strings.TrimSpace(instr), "\n\n")
}

type Group struct {
	Questions []rune
	NumPax    int
}

func IsRuneInSlice(r rune, s []rune) bool {
	for _, v := range s {
		if v == r {
			return true
		}
	}
	return false
}
