package challenge

import (
	"regexp"
	"strconv"
	"strings"
)

var (
	ruleRegex       = regexp.MustCompile(`(.+) bags contain (.+).`)
	definitionRegex = regexp.MustCompile(`(\d+) (.+) bags?`)
)

const (
	targetColour = "shiny gold"
)

func parse(instr string) map[string]map[string]int {
	inp := strings.Split(strings.TrimSpace(instr), "\n")
	rules := make(map[string]map[string]int)

	for _, rule := range inp {
		rr := ruleRegex.FindAllStringSubmatch(rule, -1)
		containerBag := rr[0][1]
		ruleSet := strings.Split(rr[0][2], ", ")

		bagRules := make(map[string]int)

		for _, definition := range ruleSet {
			rsr := definitionRegex.FindAllStringSubmatch(definition, -1)
			if len(rsr) != 0 {
				i, _ := strconv.Atoi(rsr[0][1])
				bagRules[rsr[0][2]] = i
			}
		}

		rules[containerBag] = bagRules

	}

	return rules
}
