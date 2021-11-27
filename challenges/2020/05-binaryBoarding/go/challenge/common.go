package challenge

import "strings"

var (
	front = []rune("F")[0]
	back  = []rune("B")[0]
	left  = []rune("L")[0]
	right = []rune("R")[0]
)

const (
	numRows = 128
	numCols = 8
)

func parse(instr string) []string {
	return strings.Split(strings.TrimSpace(instr), "\n")
}

func decodePosition(rowString string, decChar, incChar rune, maxVal int) int {
	minVal := 0
	maxVal -= 1

	currentRange := (maxVal + 1) - minVal

	for _, char := range strings.ToUpper(rowString) {

		rangeModifier := int(currentRange / 2)

		if char == decChar {
			maxVal -= rangeModifier
		} else if char == incChar {
			minVal += rangeModifier
		}

		currentRange /= 2

	}

	if rune(rowString[len(rowString)-1]) == decChar {
		return minVal
	}

	return maxVal
}

func parseSeat(seatString string) (int, int) {
	row := decodePosition(seatString[:7], front, back, numRows)
	col := decodePosition(seatString[7:], left, right, numCols)

	return row, col
}

func getSeatId(row, col int) int {
	return (row * 8) + col
}
