package challenge

func PartTwo(instr string) int {
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

	return treeProduct
}
