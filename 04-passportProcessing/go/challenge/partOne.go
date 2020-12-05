package challenge

import "regexp"

func PartOne(instr string) int {
	inputSlice := parse(instr)

	var valid_passports int

	testCases := []*regexp.Regexp{
		regexp.MustCompile(`byr:([^ ]+)`),
		regexp.MustCompile(`iyr:([^ ]+)`),
		regexp.MustCompile(`eyr:([^ ]+)`),
		regexp.MustCompile(`hgt:([^ ]+)`),
		regexp.MustCompile(`hcl:([^ ]+)`),
		regexp.MustCompile(`ecl:([^ ]+)`),
		regexp.MustCompile(`pid:([^ ]+)`),
	}

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

	return valid_passports
}
