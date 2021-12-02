package challenge

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

const (
	FORWARD = "forward"
	DOWN    = "down"
	UP      = "up"
)

type instruction struct {
	Direction string
	Magnitude int
}

func parse(instr string) ([]*instruction, error) {
	var o []*instruction
	for _, line := range strings.Split(strings.TrimSpace(instr), "\n") {
		splitLine := strings.Split(line, " ")
		if len(splitLine) != 2 {
			return nil, fmt.Errorf("malformed instruction %#v", line)
		}

		magnitudeInt, err := strconv.Atoi(splitLine[1])
		if err != nil {
			return nil, err
		}

		o = append(o, &instruction{
			Direction: splitLine[0],
			Magnitude: magnitudeInt,
		})
	}
	return o, nil
}

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	var depth, horizontal int

	instructions, err := parse(instr)
	if err != nil {
		return nil, err
	}

	for _, instruction := range instructions {

		switch instruction.Direction {
		case FORWARD:
			horizontal += instruction.Magnitude
		case UP:
			depth -= instruction.Magnitude
		case DOWN:
			depth += instruction.Magnitude
		default:
			return nil, fmt.Errorf("unknown direction %#v", instruction.Direction)
		}

	}

	return depth * horizontal, nil
}

func (c Challenge) Two(instr string) (interface{}, error) {
	var depth, horizontal, aim int

	instructions, err := parse(instr)
	if err != nil {
		return nil, err
	}

	for _, instruction := range instructions {

		switch instruction.Direction {
		case FORWARD:
			horizontal += instruction.Magnitude
			depth += instruction.Magnitude * aim
		case UP:
			aim -= instruction.Magnitude
		case DOWN:
			aim += instruction.Magnitude
		default:
			return nil, fmt.Errorf("unknown direction %#v", instruction.Direction)
		}

	}

	return depth * horizontal, nil
}
