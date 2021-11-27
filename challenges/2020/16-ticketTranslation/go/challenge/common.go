package challenge

import (
	"strconv"
	"strings"
)

type rule struct {
	Name   string
	Ranges [4]int
}

func newRule(instr string) rule {
	insplit := strings.Split(strings.TrimSpace(instr), ": ")
	field := insplit[0]
	conditions := insplit[1]
	ranges := strings.Split(conditions, "or")
	var rangeArray [4]int
	for i, sub := range ranges {
		x := strings.Split(strings.TrimSpace(sub), "-")
		xoi, err := strconv.Atoi(x[0])
		if err != nil {
			panic(err)
		}
		xti, err := strconv.Atoi(x[1])
		if err != nil {
			panic(err)
		}

		rangeArray[i*2] = xoi
		rangeArray[(i*2)+1] = xti
	}
	return rule{
		Name:   field,
		Ranges: rangeArray,
	}
}

type ticket struct {
	fields []int
}

func newTicket(instr string) ticket {
	insplit := strings.Split(strings.TrimSpace(instr), ",")
	var o []int
	for _, x := range insplit {
		i, err := strconv.Atoi(x)
		if err != nil {
			panic(err)
		}
		o = append(o, i)
	}
	return ticket{
		fields: o,
	}
}

func parse(instr string) ([]rule, ticket, []ticket) {

	splitInput := strings.Split(strings.TrimSpace(instr), "\n\n")

	var rules []rule
	var myTicket ticket
	var otherTickets []ticket

	for _, x := range strings.Split(splitInput[0], "\n") {
		rules = append(rules, newRule(x))
	}

	splitMyTicket := strings.Split(splitInput[1], "\n")
	myTicket = newTicket(splitMyTicket[len(splitMyTicket)-1])

	for _, x := range strings.Split(splitInput[2], "\n")[1:] {
		otherTickets = append(otherTickets, newTicket(x))
	}

	return rules, myTicket, otherTickets
}

func testValue(value int, condition [4]int) bool {
	return (condition[0] <= value && value <= condition[1]) || (condition[2] <= value && value <= condition[3])
}

func findInvalid(rules []rule, tickets []ticket) ([]int, []int) {
	var invalidValues []int
	var invalidIndexes []int

	for i, ticket := range tickets {
		for _, field := range ticket.fields {
			var fieldIsValid bool
			for _, rule := range rules {
				if testValue(field, rule.Ranges) {
					fieldIsValid = true
					break
				}
			}
			if !fieldIsValid {
				invalidValues = append(invalidValues, field)
				invalidIndexes = append(invalidIndexes, i)
			}
		}
	}

	return invalidValues, invalidIndexes
}
