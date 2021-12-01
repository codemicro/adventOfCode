package challenge

import (
	"strconv"
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

func parse(instr string) ([]int, error) {
	var o []int
	for _, line := range strings.Split(instr, "\n") {
		if line == "" {
			continue
		}
		t := strings.TrimSpace(line)
		n, err := strconv.Atoi(t)
		if err != nil {
			return nil, err
		}
		o = append(o, n)
	}
	return o, nil
}

func countIncreases(data []int) int {
	var c int
	for i := 1; i < len(data); i += 1 {
		if data[i] > data[i-1] {
			c += 1
		}
	}
	return c
}

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	data, err := parse(instr)
	if err != nil {
		return nil, err
	}
	return countIncreases(data), nil
}

func (c Challenge) Two(instr string) (interface{}, error) {
	data, err := parse(instr)
	if err != nil {
		return nil, err
	}

	var sums []int
	{
		for i := 0; i < len(data)-2; i += 1 {
			sums = append(sums, data[i]+data[i+1]+data[i+2])
		}
	}

	return countIncreases(sums), nil
}
