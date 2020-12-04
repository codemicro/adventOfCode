package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	inputBytes, _ := ioutil.ReadFile("input.txt")
	inputSlice := strings.Split(strings.TrimSpace(string(inputBytes)), "\n\n")

	for i, x := range inputSlice {
		inputSlice[i] = strings.ReplaceAll(x, "\n", " ")
	}

	var passports []Passport
	for _, x := range inputSlice {
		passports = append(passports, NewPassport(x))
	}

	var validPassports int
	for _, passport := range passports {
		if passport.Validate() {
			validPassports += 1
		}
	}

	fmt.Printf("There are %d valid passports.", validPassports)

}

type Passport struct {
	byr string // Birth year
	iyr string // Issue year
	eyr string // Expiration year
	hgt string // Height
	hcl string // Hair colour
	ecl string // Eye colour
	pid string // Passport ID
	cid string // Country ID
}

func (p Passport) Validate() bool {
	// byr (Birth Year) - four digits; at least 1920 and at most 2002.
	if p.byr == "" {
		return false
	}
	{
		i, _ := strconv.Atoi(p.byr)
		if !(1920 <= i && i <= 2002) {
			return false
		}
	}

	// iyr (Issue Year) - four digits; at least 2010 and at most 2020.
	if p.iyr == "" {
		return false
	}
	{
		i, _ := strconv.Atoi(p.iyr)
		if !(2010 <= i && i <= 2020) {
			return false
		}
	}

	// eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
	if p.eyr == "" {
		return false
	}
	{
		i, _ := strconv.Atoi(p.eyr)
		if !(2020 <= i && i <= 2030) {
			return false
		}
	}

	// hgt (Height) - a number followed by either cm or in:
	//     If cm, the number must be at least 150 and at most 193.
	//     If in, the number must be at least 59 and at most 76.
	if p.hgt == "" {
		return false
	}
	if strings.Contains(p.hgt, "cm") {
		i, _ := strconv.Atoi(strings.Trim(p.hgt, "cm"))
		if !(150 <= i && i <= 193) {
			return false
		}
	} else if strings.Contains(p.hgt, "in") {
		i, _ := strconv.Atoi(strings.Trim(p.hgt, "in"))
		if !(59 <= i && i <= 76) {
			return false
		}
	} else {
		return false
	}

	// hcl (Hair Color) - a // followed by exactly six characters 0-9 or a-f.
	if p.hcl == "" {
		return false
	}
	if p.hcl[0] == []byte("#")[0] {
		if m, _ := regexp.MatchString(`#[0-9a-f]{6}`, p.hcl); !m {
			return false
		}
	} else {
		return false
	}

	// ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
	if p.ecl == "" {
		return false
	}
	{
		var contained bool
		for _, v := range []string{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"} {
			if p.ecl == v {
				contained = true
				break
			}
		}
		if !contained {
			return false
		}
	}

	// pid (Passport ID) - a nine-digit number, including leading zeroes.
	if len(p.pid) == 9 {
		_, err := strconv.Atoi(p.pid)
		if err != nil {
			return false
		}
	} else {
		return false
	}

	return true
}

func NewPassport(instr string) Passport {
	np := Passport{}
	np.byr = extractField("byr", instr)
	np.iyr = extractField("iyr", instr)
	np.eyr = extractField("eyr", instr)
	np.hgt = extractField("hgt", instr)
	np.hcl = extractField("hcl", instr)
	np.ecl = extractField("ecl", instr)
	np.pid = extractField("pid", instr)
	np.cid = extractField("cid", instr)
	return np
}

func extractField(field, instr string) string {
	fieldRegex := regexp.MustCompile(field + `:([^ ]+)`)
	matches := fieldRegex.FindAllStringSubmatch(instr, -1)
	if len(matches) == 0 {
		return ""
	}
	return matches[0][1]
}
