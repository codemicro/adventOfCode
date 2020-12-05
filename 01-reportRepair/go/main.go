package main

import (
	"adventOfCode/01-reportRepair/go/challenge"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"runtime"
	"strconv"

	"github.com/fatih/color"
)

const (
	year  = "2020"
	day   = "1"
	title = "Report Repair"
)

func main() {
	fmt.Fprintf(color.Output, "%s: day %s - %s\n", color.YellowString("AoC "+year), color.BlueString(day), title)
	fmt.Fprintf(color.Output, "Go %s\n\n", color.BlueString(runtime.Version()))

	var challengeInput string
	{
		inb, err := ioutil.ReadFile("input.txt")
		if err != nil {
			fmt.Println("Error: could not open input.txt")
			os.Exit(-1)
		}
		challengeInput = string(inb)
	}

	runTests()

	fmt.Println("Answers")
	fmt.Fprintf(color.Output, "Part %s: %s\n", color.BlueString("1"), color.BlueString(strconv.Itoa(challenge.PartOne(challengeInput))))
	fmt.Fprintf(color.Output, "Part %s: %s\n", color.BlueString("2"), color.BlueString(strconv.Itoa(challenge.PartTwo(challengeInput))))

}

type tc struct {
	Input    string `json:"input"`
	Expected int    `json:"expected"`
}

func runTests() {

	testCases := struct {
		One []tc `json:"one"`
		Two []tc `json:"two"`
	}{}

	{
		inb, err := ioutil.ReadFile("testCases.json")
		if err != nil {
			fmt.Println("Error: could not open testCases.json. Skipping tests")
			return
		}
		err = json.Unmarshal(inb, &testCases)
		if err != nil {
			fmt.Println("Error: could not parse testCases.json. Skipping tests")
			return
		}
	}

	fmt.Println("Test cases")

	rt := func(tcs []tc, f func(string) int, n string) {
		for i, tc := range tcs {
			fmt.Fprintf(color.Output, "%s ", color.BlueString(n+"."+strconv.Itoa(i+1)))
			result := f(tc.Input)
			if result == tc.Expected {
				fmt.Fprintf(color.Output, "%s", color.GreenString("pass"))
			} else {
				fmt.Fprintf(color.Output, "%s (got %s, expected %s)", color.RedString("fail"), color.BlueString(strconv.Itoa(result)), color.BlueString(strconv.Itoa(tc.Expected)))
			}
			fmt.Println()
		}
	}

	rt(testCases.One, challenge.PartOne, "1")
	rt(testCases.Two, challenge.PartTwo, "2")

	fmt.Println()

}
