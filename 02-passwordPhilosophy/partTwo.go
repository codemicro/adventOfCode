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
	positionOne  int
	positionTwo  int
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

	fmt.Printf("There are %d valid passwords.\n", num_valid_passwords)
}
