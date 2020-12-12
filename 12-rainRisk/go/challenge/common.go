package challenge

import (
	"fmt"
	"strconv"
	"strings"
)

type Instruction struct {
	Action    string
	Magnitude int
	Raw       string
}

func NewInstruction(rawIns string) Instruction {
	ci, err := strconv.Atoi(rawIns[1:])
	if err != nil {
		panic(err)
	}
	return Instruction{
		Action:    strings.ToLower(string(rawIns[0])),
		Magnitude: ci,
		Raw:       rawIns,
	}
}

func calculateDirectionDeltas(direction string, amount int) (int, int) {
	var (
		latDelta  int
		longDelta int
	)

	if direction == "n" {
		latDelta += amount
	} else if direction == "s" {
		latDelta -= amount
	} else if direction == "e" {
		longDelta += amount
	} else if direction == "w" {
		longDelta -= amount
	} else {
		panic(fmt.Errorf("invalid direction '%s'", direction))
	}

	return latDelta, longDelta
}

func parse(instr string) (o []Instruction) {
	for _, v := range strings.Split(strings.TrimSpace(instr), "\n") {
		o = append(o, NewInstruction(v))
	}
	return
}
