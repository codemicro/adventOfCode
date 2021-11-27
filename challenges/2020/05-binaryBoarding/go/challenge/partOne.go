package challenge

func PartOne(instr string) int {
	inputSlice := parse(instr)

	var highestSeatId int
	for _, seat := range inputSlice {
		psr, psc := parseSeat(seat)
		seatId := getSeatId(psr, psc)
		if seatId > highestSeatId {
			highestSeatId = seatId
		}
	}

	return highestSeatId
}
