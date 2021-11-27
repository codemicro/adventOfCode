package challenge

func checkBag(ruleset map[string]map[string]int, testCl, targetCl string) bool {
	{
		var isPresent bool
		for v := range ruleset[testCl] {
			if v == targetCl {
				isPresent = true
				break
			}
		}
		if isPresent {
			return true
		}
	}

	for childColour := range ruleset[testCl] {
		if checkBag(ruleset, childColour, targetCl) {
			return true
		}
	}

	return false

}

func PartOne(instr string) int {
	rules := parse(instr)

	canContainTarget := 0

	for bagColour, _ := range rules {
		if bagColour != targetColour {
			if checkBag(rules, bagColour, targetColour) {
				canContainTarget += 1
			}
		}
	}

	return canContainTarget
}
