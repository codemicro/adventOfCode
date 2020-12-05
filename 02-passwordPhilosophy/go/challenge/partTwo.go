package challenge

import (
	"strconv"
)

func PartTwo(instr string) int {
	inputSlice := parse(instr)

	type Password struct {
		plaintext    string
		targetLetter rune
		positionOne  int
		positionTwo  int
	}

	var passwords []Password
	for _, line := range inputSlice {
		matches := parserRegex.FindAllStringSubmatch(line, -1)
		miR, _ := strconv.Atoi(matches[0][1])
		maR, _ := strconv.Atoi(matches[0][2])
		passwords = append(passwords, Password{
			plaintext:    matches[0][4],
			targetLetter: rune(matches[0][3][0]),
			positionOne:  miR - 1,
			positionTwo:  maR - 1,
		})
	}

	var num_valid_passwords int

	for _, password := range passwords {
		positionOneMatches := rune(password.plaintext[password.positionOne]) == password.targetLetter
		positionTwoMatches := rune(password.plaintext[password.positionTwo]) == password.targetLetter

		if positionOneMatches != positionTwoMatches {
			num_valid_passwords += 1
		}
	}

	return num_valid_passwords
}
