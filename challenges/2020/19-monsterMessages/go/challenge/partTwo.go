package challenge

import (
	"regexp"
	"strings"
)

func PartTwo(instr string) int {

	// patch input
	instr = strings.ReplaceAll(instr, "8: 42", "8: 42 | 42 8")
	instr = strings.ReplaceAll(instr, "11: 42 31", "11: 42 31 | 42 11 31")

	rules, messages := parse(instr)

	// Since we have sections of our ruleset, we have markers in the regex returned by `make_ruleset_regex`
	// that denote where we need to insert a copy of the rule 11 regular expression (which also happens to
	// have one of those markers in it)

	rr := makeRulesetRegex(rules)
	elevenRegex := generateRuleRegex(rules, 11)
	for i := 0; i < 10; i += 2 {
		rr = strings.ReplaceAll(rr, replaceMarker, elevenRegex)
	}

	// run as usual
	ruleRegex := regexp.MustCompile(rr)
	return run(messages, ruleRegex)
}
