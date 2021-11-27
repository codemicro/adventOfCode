package challenge

import "strings"

func parse(instr string) [][]rune {
	inputSlice := strings.Split(strings.TrimSpace(instr), "\n")

	var forest [][]rune
	for _, line := range inputSlice {
		forest = append(forest, []rune(line))
	}
	return forest
}

var tree_char = []rune("#")[0] // No idea why I can't just do rune("#")

func findCollisions(forest [][]rune, xOffset, yOffset int) int {
	var encounteredTrees int
	var xPointer int
	var yPointer int

	for yPointer < len(forest) {
		row := forest[yPointer]
		targetIndex := xPointer % len(row)
		if row[targetIndex] == tree_char {
			encounteredTrees += 1
		}
		xPointer += xOffset
		yPointer += yOffset
	}

	return encounteredTrees
}
