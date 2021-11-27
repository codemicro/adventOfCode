package challenge

func countForBag(ruleset map[string]map[string]int, testCl string) int {
	if len(ruleset[testCl]) == 0 {
		return -1
	}

	count := 0

	for childColour := range ruleset[testCl] {
		childBags := countForBag(ruleset, childColour)
		var v int
		if childBags == -1 {
			v = ruleset[testCl][childColour]
		} else {
			v = ruleset[testCl][childColour] * childBags
			v += ruleset[testCl][childColour]
		}
		count += v
	}

	return count

}

func PartTwo(instr string) int {
	return countForBag(parse(instr), targetColour)
}
