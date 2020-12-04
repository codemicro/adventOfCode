package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strings"
)

var testCases = []*regexp.Regexp{
	regexp.MustCompile(`byr:([^ ]+)`),
	regexp.MustCompile(`iyr:([^ ]+)`),
	regexp.MustCompile(`eyr:([^ ]+)`),
	regexp.MustCompile(`hgt:([^ ]+)`),
	regexp.MustCompile(`hcl:([^ ]+)`),
	regexp.MustCompile(`ecl:([^ ]+)`),
	regexp.MustCompile(`pid:([^ ]+)`),
}

func main() {
	inputBytes, _ := ioutil.ReadFile("input.txt")
	inputSlice := strings.Split(strings.TrimSpace(string(inputBytes)), "\n\n")

	for i, x := range inputSlice {
		inputSlice[i] = strings.ReplaceAll(x, "\n", " ")
	}

	var valid_passports int

	for _, passport := range inputSlice {
		valid := true
		for _, tc := range testCases {
			if !tc.MatchString(passport) {
				valid = false
				break
			}
		}

		if valid {
			valid_passports += 1
		}

	}

	fmt.Printf("There are %d valid passports.\n", valid_passports)

}
