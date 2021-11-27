package challenge

import (
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

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

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	return findCollisions(parse(instr), 3, 1), nil
}

func (c Challenge) Two(instr string) (interface{}, error) {
	forest := parse(instr)

	offsetPairs := [][]int{
		{3, 1},
		{1, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}

	treeProduct := 1

	for _, pair := range offsetPairs {
		encounteredTrees := findCollisions(forest, pair[0], pair[1])
		treeProduct *= encounteredTrees
	}

	return treeProduct, nil
}
