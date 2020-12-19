package challenge

import "regexp"

func PartOne(instr string) int {
	rules, messages := parse(instr)
	ruleRegex := regexp.MustCompile(makeRulesetRegex(rules))
	return run(messages, ruleRegex)
}
