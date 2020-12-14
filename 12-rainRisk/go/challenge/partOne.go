package challenge

import "fmt"

var (
	bearingsNum = map[int]string{
		0:   "n",
		90:  "e",
		180: "s",
		270: "w",
	}

	bearingsLtr = map[string]int{
		"n": 0,
		"e": 90,
		"s": 180,
		"w": 270,
	}
)

func rotateDirection(current string, direction string, amount int) string {
	if !(direction == "l" || direction == "r") {
		panic(fmt.Errorf("invalid rotate direction '%s'", direction))
	}
	currentBearing := bearingsLtr[current]

	if direction == "l" {
		currentBearing -= amount
	} else if direction == "r" {
		currentBearing += amount
	}

	if currentBearing >= 360 {
		currentBearing -= 360
	} else if currentBearing < 0 {
		currentBearing += 360
	}

	return bearingsNum[currentBearing]
}

func translateMovementOne(currentDirection string, instruction Instruction) (string, int, int) {
	// Returns the new current direction and the lat/long delta

	latDelta := 0
	longDelta := 0

	if instruction.Action == "l" || instruction.Action == "r" {
		currentDirection = rotateDirection(currentDirection, instruction.Action, instruction.Magnitude)
	} else if instruction.Action == "f" {
		latDelta, longDelta = calculateDirectionDeltas(currentDirection, instruction.Magnitude)
	} else if instruction.Action == "n" || instruction.Action == "s" || instruction.Action == "e" || instruction.Action == "w" {
		latDelta, longDelta = calculateDirectionDeltas(instruction.Action, instruction.Magnitude)
	} else {
		panic(fmt.Errorf("invalid action '%s'", instruction.Action))
	}

	return currentDirection, latDelta, longDelta

}

func PartOne(instr string) int {
	inputSlice := parse(instr)

	currentDirection := "e"
	lat := 0
	long := 0

	for _, instruction := range inputSlice {
		var (
			lad int
			lod int
		)
		currentDirection, lad, lod = translateMovementOne(currentDirection, instruction)
		lat += lad
		long += lod
	}

	if lat < 0 {
		lat = lat + -2*lat
	}
	if long < 0 {
		long = long + -2*long
	}

	return lat + long
}
