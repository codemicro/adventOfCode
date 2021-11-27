package challenge

func PartTwo(instr string) int {
	inputSlice := parse(instr)

	var seatMatrix [numRows][numCols]bool
	for _, seat := range inputSlice {
		row, col := parseSeat(seat)
		seatMatrix[row][col] = true
	}

	var (
		lastOne bool
		lastTwo bool
	)

	for row := 0; row < len(seatMatrix); row += 1 {
		for col := 0; col < len(seatMatrix[row]); col += 1 {
			this := seatMatrix[row][col]
			if lastTwo && !lastOne && this {
				// We need to get the previous item because at this point, we've already moved on one
				prevRow := row
				prevCol := col - 1
				if prevCol < 0 {
					prevRow -= 1
					prevCol += numCols
				}
				return getSeatId(prevRow, prevCol)
			}
			lastTwo = lastOne
			lastOne = this
		}
	}

	return 0
}
