package challenge


func getNewStateOne(numNeighbours int, oldState rune) rune {
	if numNeighbours == 0 {
		return filledSeat
	} else if numNeighbours >= 4 && oldState == filledSeat {
		return openSeat
	}
	return oldState
}

func countNeighboursOne(hall [][]rune, currentPos [2]int, hallSize [2]int) (numNeighbours int) {
	row := currentPos[0]
	col := currentPos[1]

	for _, position := range lookupPositions {
		test_x_pos := position[0] + col
		test_y_pos := position[1] + row

		if 0 <= test_x_pos && test_x_pos < hallSize[0] && 0 <= test_y_pos && test_y_pos < hallSize[1] {
			if hall[test_y_pos][test_x_pos] == filledSeat {
				numNeighbours += 1
			}
		}
	}
	
	return
}

func PartOne(instr string) int {
	return run(parse(instr), countNeighboursOne, getNewStateOne)
}