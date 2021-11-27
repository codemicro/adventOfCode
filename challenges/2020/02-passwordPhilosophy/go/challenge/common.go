package challenge

import (
	"regexp"
	"strings"
)

func parse(instr string) []string {
	return strings.Split(strings.TrimSpace(string(instr)), "\n")
}

var parserRegex = regexp.MustCompile(`(?m)(\d+)-(\d+) ([a-z]): (.+)`)
