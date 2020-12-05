package challenge

func PartTwo(instr string) int {
	values := parse(instr)

	for _, i := range values {
		for _, v := range values {
			for _, x := range values {
				if v+i+x == 2020 {
					return v * i * x
				}
			}
		}
	}

	return 0
}
