package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"
)

type Password struct {
	plaintext    string
	targetLetter rune
	minRepeats   int
	maxRepeats   int
}

var parserRegex = regexp.MustCompile(`(?m)(\d+)-(\d+) ([a-z]): (.+)`)

func main() {
	inputBytes, _ := ioutil.ReadFile("input.txt")
	inputSlice := strings.Split(strings.TrimSpace(string(inputBytes)), "\n")

	var passwords []Password
	for _, line := range inputSlice {
		matches := parserRegex.FindAllStringSubmatch(line, -1)
		miR, _ := strconv.Atoi(matches[0][1])
		maR, _ := strconv.Atoi(matches[0][2])
		passwords = append(passwords, Password{
			plaintext:    matches[0][4],
			targetLetter: rune(matches[0][3][0]),
			minRepeats:   miR,
			maxRepeats:   maR,
		})
	}

	var num_valid_passwords int

	for _, password := range passwords {
		var target_letter_count int
		for _, char := range password.plaintext {
			if char == password.targetLetter {
				target_letter_count += 1
			}
		}

		if (target_letter_count >= password.minRepeats) && (target_letter_count <= password.maxRepeats) {
			num_valid_passwords += 1
		}
	}

	fmt.Printf("There are %d valid passwords.\n", num_valid_passwords)
}
