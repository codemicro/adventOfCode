package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

var tree_char = []rune("#")[0] // No idea why I can't just do rune("#")

func main() {
	inputBytes, _ := ioutil.ReadFile("input.txt")
	inputSlice := strings.Split(strings.TrimSpace(string(inputBytes)), "\n")

	var forest [][]rune
	for _, line := range inputSlice {
		forest = append(forest, []rune(line))
	}

	offsetPairs := [][]int{
		{3, 1},
		{1, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}

	treeProduct := 1

	for i, pair := range offsetPairs {
		encounteredTrees := findCollisions(forest, pair[0], pair[1])
		treeProduct *= encounteredTrees
		fmt.Printf("Pair %d: %d trees", i, encounteredTrees)
		if i == 0 {
			fmt.Print(" (part one solution)")
		}
		fmt.Println()
	}

	fmt.Printf("Product of all: %d (part two solution)\n", treeProduct)

}

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
