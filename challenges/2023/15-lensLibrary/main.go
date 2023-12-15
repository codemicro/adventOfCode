package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func hash(x string) int {
	var res int
	for _, char := range x {
		res += int(char)
		res *= 17
		res = res % 256
	}
	return res
}

func parse(instr string) []string {
	return strings.Split(instr, ",")
}

func one(instr string) int {
	var (
		sequence = parse(instr)
		acc      int
	)

	for _, section := range sequence {
		acc += hash(section)
	}

	return acc
}

type lens struct {
	Label       string
	FocalLength int
}

func parseLens(x string) (*lens, rune) {
	var (
		op               rune
		labelRunes       []rune
		foundFocalLength bool
		focalLengthRunes []rune
	)

	for _, char := range x {
		if char == '-' {
			op = char
			break
		}

		if char == '=' {
			op = char
			foundFocalLength = true
			continue
		}

		if foundFocalLength {
			focalLengthRunes = append(focalLengthRunes, char)
		} else {
			labelRunes = append(labelRunes, char)
		}
	}

	res := new(lens)

	if foundFocalLength {
		var err error
		res.FocalLength, err = strconv.Atoi(string(focalLengthRunes))
		if err != nil {
			panic(err)
		}
	}

	res.Label = string(labelRunes)

	return res, op
}

func two(instr string) int {
	sequence := parse(instr)

	boxes := make([][]*lens, 256)

	for _, part := range sequence {
		var (
			lens, op = parseLens(part)
			labelHash = hash(lens.Label)
			added bool
		)

		var n int
		for _, x := range boxes[labelHash] {
			if labelMatches := x.Label == lens.Label; labelMatches && op == '=' {
				added = true
				boxes[labelHash][n] = lens
				n += 1
			} else if !labelMatches {
				boxes[labelHash][n] = x
				n += 1
			}
		}
		boxes[labelHash] = boxes[labelHash][:n]

		if !added && op == '=' {
			boxes[labelHash] = append(boxes[labelHash], lens)
		}
	}

	var acc int
	for i, box := range boxes {
		for j, lens := range box {
			acc += (i + 1) * (j + 1) * lens.FocalLength
		}
	}
	return acc
}

func main() {
	if len(os.Args) < 2 || !(os.Args[1] == "1" || os.Args[1] == "2") {
		debug("Missing day argument")
		os.Exit(1)
	}

	inp, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	inpStr := strings.TrimSpace(string(inp))

	switch os.Args[1] {
	case "1":
		fmt.Println(one(inpStr))
	case "2":
		fmt.Println(two(inpStr))
	}
}

func debug(f string, sub ...any) {
	fmt.Fprintf(os.Stderr, f, sub...)
}
