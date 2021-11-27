package challenge

import (
	"errors"
	"strconv"
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	values := parse(instr)

	for _, i := range values {
		for _, v := range values {
			if v+i == 2020 {
				return v * i, nil
			}
		}
	}

	return nil, errors.New("no combinations found")
}

func (c Challenge) Two(instr string) (interface{}, error) {
	values := parse(instr)

	for _, i := range values {
		for _, v := range values {
			for _, x := range values {
				if v+i+x == 2020 {
					return v * i * x, nil
				}
			}
		}
	}

	return nil, errors.New("no combinations found")
}

func parse(instr string) []int {
	inputSlice := strings.Split(strings.TrimSpace(instr), "\n")

	var values []int
	for _, v := range inputSlice {
		str, _ := strconv.Atoi(v)
		values = append(values, str)
	}

	return values
}
