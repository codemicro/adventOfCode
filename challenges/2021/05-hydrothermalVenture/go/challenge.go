package challenge

import (
	"strconv"
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

type Point struct {
	x int
	y int
}

func pointFromString(input string) (*Point, error) {
	sp := strings.Split(input, ",")
	x, err := strconv.Atoi(sp[0])
	if err != nil {
		return nil, err
	}
	y, err := strconv.Atoi(sp[1])
	if err != nil {
		return nil, err
	}
	return &Point{x: x, y: y}, nil
}

type Line [2]*Point

func parse(instr string) ([]Line, error) {
	var o []Line
	for _, line := range strings.Split(strings.TrimSpace(instr), "\n") {
		sp := strings.Split(line, " -> ")
		p1, err := pointFromString(sp[0])
		if err != nil {
			return nil, err
		}
		p2, err := pointFromString(sp[1])
		if err != nil {
			return nil, err
		}
		o = append(o, Line{p1, p2})
	}
	return o, nil
}

func removeDiagonalLines(lines []Line) []Line {
	var n int
	for _, line := range lines {
		if line[0].x == line[1].x || line[0].y == line[1].y {
			lines[n] = line
			n += 1
		}
	}
	return lines[:n]
}

func iteratePoints(line Line) chan *Point {

	p1 := line[0]
	p2 := line[1]

	delta_x := p2.x - p1.x
	delta_y := p2.y - p1.y

	var xStep, yStep int

	if delta_x > 0 {
		xStep = 1
	} else if delta_x < 0 {
		xStep = -1
	}

	if delta_y > 0 {
		yStep = 1
	} else if delta_y < 0 {
		yStep = -1
	}

	c := make(chan *Point)

	go func() {
		c <- p1
		lastPoint := *p1
		for lastPoint != *p2 {
			np := &Point{
				x: lastPoint.x + xStep,
				y: lastPoint.y + yStep,
			}
			c <- np
			lastPoint = *np
		}
		close(c)
	}()

	return c
}

func countOverlappingPoints(lines []Line) int {
	areas := make(map[Point]int)
	for _, line := range lines {
		for point := range iteratePoints(line) {
			t := *point
			areas[t] = areas[t] + 1
		}
	}

	var numberOverlaps int
	for _, n := range areas {
		if n > 1 {
			numberOverlaps += 1
		}
	}
	return numberOverlaps
}

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	lines, err := parse(instr)
	if err != nil {
		return nil, err
	}
	lines = removeDiagonalLines(lines)
	return countOverlappingPoints(lines), nil
}

func (c Challenge) Two(instr string) (interface{}, error) {
	lines, err := parse(instr)
	if err != nil {
		return nil, err
	}
	return countOverlappingPoints(lines), nil
}
