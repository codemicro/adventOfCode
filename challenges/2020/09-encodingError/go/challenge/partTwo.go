package challenge

func PartTwo(instr string) int {
	inputSlice := parse(instr)

	targetValue := PartOne(instr)
	if targetValue == 0 {
		return 0
	}

	var pointer int
	for pointer < len(inputSlice) {
		startPoint := pointer
		iptr := pointer
		var count int
		for iptr < len(inputSlice) {
			count += inputSlice[iptr]

			if count == targetValue {
				if iptr-startPoint < 2 {
					break
				}

				allValues := inputSlice[startPoint : iptr+1]
				min := allValues[0]
				max := allValues[0]
				for _, v := range allValues {
					if v < min {
						min = v
					}
					if v > max {
						max = v
					}
				}
				return min + max
			}

			if count > targetValue {
				break
			}

			iptr += 1
		}

		pointer += 1
	}

	return 0
}
