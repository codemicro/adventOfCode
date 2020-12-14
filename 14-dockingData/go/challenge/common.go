package challenge

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

type Instruction struct {
	Address int
	Value   int
	Mask    string
}

var instructionRegex = regexp.MustCompile(`mem\[(\d+)\] ?= ?(\d+)`)

func NewInstruction(instruction, mask string) Instruction {
	if mask == "" {
		panic(errors.New("bad mask"))
	}
	if !instructionRegex.MatchString(instruction) {
		panic(fmt.Errorf("unable to parse input instruction '%s'", instruction))
	}
	matches := instructionRegex.FindAllStringSubmatch(instruction, -1)
	address, err := strconv.Atoi(matches[0][1])
	if err != nil {
		panic(err)
	}
	value, err := strconv.Atoi(matches[0][2])
	if err != nil {
		panic(err)
	}
	return Instruction{
		Address: address,
		Value:   value,
		Mask:    mask,
	}
}

func parse(instr string) (retval []Instruction) {

	var currentMask string
	for _, line := range strings.Split(strings.TrimSpace(instr), "\n") {
		if strings.Contains(line, "mask") {
			currentMask = strings.TrimSpace(strings.Split(line, "=")[1])
		} else {
			retval = append(retval, NewInstruction(line, currentMask))
		}
	}

	return
}

func numberToBase(n, b int) string {
	if n == 0 {
		return "0"
	}
	var digits []int
	for n != 0 {
		digits = append(digits, n%b)
		n /= b
	}
	var sarr []string
	for i := len(digits) - 1; i >= 0; i -= 1 {
		sarr = append(sarr, strconv.Itoa(digits[i]))
	}
	return strings.Join(sarr, "")
}

func zfill(instr string, n int) string {
	for i := 0; i < n; i += 1 {
		instr = "0" + instr
	}
	return instr
}