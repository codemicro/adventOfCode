package challenge

func PartOne(instr string) int {
	rules, _, tickets := parse(instr)
	invalidValues, _ := findInvalid(rules, tickets)

	var sigma int
	for _, v := range invalidValues {
		sigma += v
	}

	return sigma
}
