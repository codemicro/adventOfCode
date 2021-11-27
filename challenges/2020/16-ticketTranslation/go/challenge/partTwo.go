package challenge

import (
	"sort"
	"strings"

	mapset "github.com/deckarep/golang-set"
)

func PartTwo(instr string) int {
	rules, myTicket, tickets := parse(instr)

	// purge bad indexes
	_, invalidIndexes := findInvalid(rules, tickets)
	sort.Ints(invalidIndexes)

	for i := len(invalidIndexes) - 1; i >= 0; i -= 1 { // iterate backwards
		idx := invalidIndexes[i]
		tickets = append(tickets[:idx], tickets[idx+1:]...)
	}

	ticketLength := len(tickets[0].fields)

	// And with this I have broken my unwritten rule of no external libraries...
	// Oh well. I like sets.
	candidates := make(map[string]mapset.Set)
	for _, rule := range rules {
		candidates[rule.Name] = mapset.NewSet()
	}

	for col := 0; col < ticketLength; col += 1 {
		var values []int
		for _, ticket := range tickets {
			values = append(values, ticket.fields[col])
		}

		for _, rule := range rules {
			completeMatch := true
			for _, v := range values {
				if !testValue(v, rule.Ranges) {
					completeMatch = false
					break
				}
			}

			if completeMatch {
				// pleeeeease give us map pointers
				// please
				x := candidates[rule.Name]
				x.Add(col)
				candidates[rule.Name] = x
			}
		}
	}

	parameterIndexes := make(map[string]int)
	removed := mapset.NewSet()

	for col := 0; col < ticketLength; col += 1 {
		for name, cset := range candidates {
			candidatesSet := cset.Difference(removed)

			if candidatesSet.Cardinality() == 1 {
				idx := candidatesSet.Pop().(int)
				parameterIndexes[name] = idx
				removed.Add(idx)
			}
		}
	}

	product := 1
	for param, v := range parameterIndexes {
		if strings.Contains(param, "departure") {
			product *= myTicket.fields[v]
		}
	}

	return product
}
