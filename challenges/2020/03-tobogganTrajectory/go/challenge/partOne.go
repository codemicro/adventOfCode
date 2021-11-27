package challenge

func PartOne(instr string) int {
	return findCollisions(parse(instr), 3, 1)
}
