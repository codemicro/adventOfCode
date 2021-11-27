package challenge

import (
	"reflect"
	"strings"
)

const (
	openSeat   = 'L'
	filledSeat = '#'
	noSeat     = '.'
)

var (
	lookupPositions = [][2]int{
		{0, 1},
		{1, 1},
		{1, 0},
		{1, -1},
		{0, -1},
		{-1, -1},
		{-1, 0},
		{-1, 1},
	}
)

func parse(instr string) (o [][]rune) {
	for _, x := range strings.Split(strings.TrimSpace(instr), "\n") {
		o = append(o, []rune(x))
	}
	return
}

func iterate(currentHall [][]rune, neighbourCounter func([][]rune, [2]int, [2]int) int, getNewState func(int, rune) rune) [][]rune {
	// Copy hall
	nextHall := make([][]rune, len(currentHall))
	for i, lc := range currentHall {
		nextHall[i] = make([]rune, len(lc))
		copy(nextHall[i], lc)
	}

	hallSize := [2]int{len(nextHall[0]), len(nextHall)}

	// iterate each chair space
	for col := 0; col < hallSize[0]; col += 1 {
		for row := 0; row < hallSize[1]; row += 1 {
			currentPos := currentHall[row][col]

			// It it's the floor, there's nothing we can do with this spot
			if currentPos == noSeat {
				continue
			}

			// Count number of adjacent seats
			numNeighbours := neighbourCounter(currentHall, [2]int{row, col}, hallSize)

			// Execute rules on copied list based on that count
			nextHall[row][col] = getNewState(numNeighbours, nextHall[row][col])

		}
	}

	return nextHall
}

func run(currentState [][]rune, neighbourCounter func([][]rune, [2]int, [2]int) int, getNewState func(int, rune) rune) int {
	lastState := make([][]rune, 0)

	for !reflect.DeepEqual(currentState, lastState) {
		lastState = currentState
		currentState = iterate(currentState, neighbourCounter, getNewState)
	}

	totalOccupied := 0
	for _, a := range currentState {
		for _, b := range a {
			if b == filledSeat {
				totalOccupied += 1
			}
		}
	}

	return totalOccupied

}
