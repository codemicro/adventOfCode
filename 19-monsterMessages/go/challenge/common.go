package challenge

import (
	"regexp"
	"strconv"
	"strings"
)

var (
	charRegex       = regexp.MustCompile(`^\"([a-z])\"$`)              // group 1 contains interesting information
	orRuleRegex     = regexp.MustCompile(`^((\d+ ?)+) \| ((\d+ ?)+)$`) // group 1 and 3 contain interesting info
	singleRuleRegex = regexp.MustCompile(`^((\d+ ?)+)$`)               // group 0 and 1 both contain the same interesting information
)

const replaceMarker = "!!!REPLACETHISMARKER!!!"

func generateCompoundRuleRegex(ruleset map[int]string, compound string, current int) string {

	// Used when you have a rule that looks like `125: 116 33 | 131 113`
	// compound should be a sequence like `116 33`
	// current should be the current rule number

	var o string

	for _, xs := range strings.Split(compound, " ") {
		x, err := strconv.Atoi(xs)
		if err != nil {
			panic(err)
		}
		if x == current {
			if x == 8 {
				o += generateRuleRegex(ruleset, 42)
				o += "+"
			} else {
				o += replaceMarker
			}
		} else {
			o += generateRuleRegex(ruleset, x)
		}
	}

	return o
}

func generateRuleRegex(ruleset map[int]string, rule int) string {

	// Rule is the integer number of the rule to generate a regular expression for
	// Said integer should correspond to a key-value pair in the ruleset

	ruleContent := ruleset[rule]

	if charRegex.MatchString(ruleContent) {
		// is a single character
		// `116: "a"`
		return charRegex.FindAllStringSubmatch(ruleContent, -1)[0][1]
	}

	// if we get here, that means there are multiple options for the rule
	// hence we need to open a new set of brackets
	output := "("

	if orRuleRegex.MatchString(ruleContent) {
		// rule is an OR rule
		// `83: 26 131 | 47 116`
		submatches := orRuleRegex.FindAllStringSubmatch(ruleContent, -1)[0]

		output += generateCompoundRuleRegex(ruleset, submatches[1], rule)
		output += "|"
		output += generateCompoundRuleRegex(ruleset, submatches[3], rule)
	} else if singleRuleRegex.MatchString(ruleContent) {
		// rule is a simple sequence rule
		// `92: 67 131`
		output += generateCompoundRuleRegex(ruleset, singleRuleRegex.FindAllStringSubmatch(ruleContent, -1)[0][1], rule)
	}

	// close original set of brackets
	output += ")"

	return output
}

func makeRulesetRegex(ruleset map[int]string) string {
	return "^" + generateRuleRegex(ruleset, 0) + "$"
}

func run(messages []string, regex *regexp.Regexp) int {
	var validInputs int
	for _, message := range messages {
		if regex.MatchString(message) {
			validInputs += 1
		}
	}
	return validInputs
}

func parse(instr string) (map[int]string, []string) {

	splitInput := strings.Split(strings.TrimSpace(instr), "\n\n")

	rules := make(map[int]string)
	for _, x := range strings.Split(splitInput[0], "\n") {
		splitRule := strings.Split(x, ":")
		num, err := strconv.Atoi(strings.TrimSpace(splitRule[0]))
		if err != nil {
			panic(err)
		}
		rules[num] = strings.TrimSpace(splitRule[1])
	}

	return rules, strings.Split(strings.TrimSpace(splitInput[1]), "\n")
}
