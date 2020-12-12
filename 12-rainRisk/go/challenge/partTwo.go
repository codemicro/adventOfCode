package challenge

import "fmt"

func makePositive(n int) int {
	if n >= 0 {
		return n
	}
	return n + -2*n
}

func makeNegative(n int) int {
	if n < 0 {
		return n
	}
	return n + -2*n
}

func rotateWaypoint(current [2]int, direction string, amount int) [2]int {
	if !(direction == "l" || direction == "r") {
		panic(fmt.Errorf("invalid rotate direction '%s'", direction))
	}

	latDelta := current[0]
	longDelta := current[1]

	times := int(amount / 90)

	var quadrant int
	if latDelta >= 0 && longDelta >= 0 {
		quadrant = 1
	} else if latDelta < 0 && longDelta >= 0 {
		quadrant = 2
	} else if latDelta < 0 && longDelta < 0 {
		quadrant = 3
	} else if latDelta >= 0 && longDelta < 0 {
		quadrant = 4
	}

	if quadrant == 0 {
		panic(fmt.Errorf("unable to determine quadrant for %d", current))
	}

	newQuadrant := quadrant
	if direction == "r" {
		newQuadrant += times
	} else if direction == "l" {
		newQuadrant -= times
	}

	if newQuadrant > 4 {
		newQuadrant -= 4
	} else if newQuadrant < 1 {
		newQuadrant += 4
	}

	quadrantDiff := quadrant - newQuadrant
	if quadrantDiff%2 != 0 {
		t := latDelta
		latDelta = longDelta
		longDelta = t
	}

	if newQuadrant == 1 {
		latDelta = makePositive(latDelta)
		longDelta = makePositive(longDelta)
	} else if newQuadrant == 2 {
		latDelta = makeNegative(latDelta)
		longDelta = makePositive(longDelta)
	} else if newQuadrant == 3 {
		latDelta = makeNegative(latDelta)
		longDelta = makeNegative(longDelta)
	} else if newQuadrant == 4 {
		latDelta = makePositive(latDelta)
		longDelta = makeNegative(longDelta)
	}

	return [2]int{latDelta, longDelta}

}

func moveToWaypoint(waypointDelta [2]int, times int) (int, int) {
	return waypointDelta[0] * times, waypointDelta[1] * times
}

func translateMovementTwo(waypointDelta [2]int, instruction Instruction) ([2]int, int, int) {
	// Returns the new current direction and the lat/long delta

	var (
		latDelta  int
		longDelta int
	)

	if instruction.Action == "l" || instruction.Action == "r" {
		waypointDelta = rotateWaypoint(waypointDelta, instruction.Action, instruction.Magnitude)
	} else if instruction.Action == "f" {
		latDelta, longDelta = moveToWaypoint(waypointDelta, instruction.Magnitude)
	} else if instruction.Action == "n" || instruction.Action == "s" || instruction.Action == "e" || instruction.Action == "w" {
		wpLatDelta, wpLongDelta := calculateDirectionDeltas(instruction.Action, instruction.Magnitude)
		waypointDelta = [2]int{wpLatDelta + waypointDelta[0], wpLongDelta + waypointDelta[1]}
	} else {
		panic(fmt.Errorf("invalid action '%s'", instruction.Action))
	}

	return waypointDelta, latDelta, longDelta
}

func PartTwo(instr string) int {
	inputSlice := parse(instr)

	waypointDelta := [2]int{1, 10}
	lat := 0
	long := 0

	for _, instruction := range inputSlice {
		var (
			lad int
			lod int
		)
		waypointDelta, lad, lod = translateMovementTwo(waypointDelta, instruction)
		lat += lad
		long += lod
	}

	if lat < 0 {
		lat = lat + -2*lat
	}
	if long < 0 {
		long = long + -2 * long
	}

	return lat + long
}
