package challenge

func PartOne(instr string) int {
	values := parse(instr)

	for _, i := range values {
		for _, v := range values {
			if v+i == 2020 {
				return v * i
			}
		}
	}

	return 0
}
