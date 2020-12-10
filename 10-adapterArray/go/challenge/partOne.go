package challenge

import (
	"sort"
	"strconv"
	"strings"
)

type Adaptor struct {
	Output   int
	MinInput int
	MaxInput int
}

func (a Adaptor) IsCompatible(inputJoltage int) bool {
	return (a.MinInput <= inputJoltage) && (a.MaxInput >= inputJoltage)
}

func NewAdaptor(outputJoltage int) Adaptor {
	return Adaptor{
		Output:   outputJoltage,
		MinInput: outputJoltage - 3,
		MaxInput: outputJoltage - 1,
	}
}

func parse(instr string) []Adaptor {
	var aslc []Adaptor
	for _, v := range strings.Split(strings.TrimSpace(instr), "\n") {
		i, err := strconv.Atoi(v)
		if err != nil {
			panic(err)
		}
		aslc = append(aslc, NewAdaptor(i))
	}

	// If I don't sort it, the recusrion in part one takes impossibly long to run
	sort.Slice(aslc, func(p, q int) bool {
		return aslc[p].Output < aslc[q].Output
	})

	return aslc
}

type ac struct {
	idx int
	adp Adaptor
}

func findChain(adaptors []Adaptor, currentJoltage int) (bool, int, int) {
	if len(adaptors) == 0 {
		return true, 0, 0
	}

	var candidates []ac
	for i, a := range adaptors {
		if a.IsCompatible(currentJoltage) {
			candidates = append(candidates, ac{i, a})
		}
	}

	if len(candidates) == 0 {
		return false, 0, 0
	}

	for _, possibleAdaptor := range candidates {
		lc := make([]Adaptor, len(adaptors))
		copy(lc, adaptors)
		lc = append(lc[:possibleAdaptor.idx], lc[possibleAdaptor.idx+1:]...)

		foundChain, numOneDiff, numThreeDiff := findChain(lc, possibleAdaptor.adp.Output)

		if foundChain {
			od := 0
			td := 0

			diff := possibleAdaptor.adp.Output - currentJoltage
			if diff == 1 {
				od += 1
			} else if diff == 3 {
				td += 1
			}

			return true, od + numOneDiff, td + numThreeDiff
		}

	}

	return false, 0, 0
	
}

func PartOne(instr string) int {
	adaptors := parse(instr)

	// Add integreated device adaptor
	var maxJ int
	{
		for _, adaptor := range adaptors {
			if maxJ < adaptor.Output {
				maxJ = adaptor.Output
			}
		}
	}
	adaptors = append(adaptors, NewAdaptor(maxJ + 3))

	s, oj, tj := findChain(adaptors, 0)

	if s {
		return oj * tj
	} 

	return 0
}
