package main

import (
	"adventOfCode/14-dockingData/go/challenge"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"runtime"
	"strconv"

	"github.com/fatih/color"
)

func main() {
	var infoStruct info
	{
		inb, err := ioutil.ReadFile("info.json")
		if err != nil {
			fmt.Println("Error: could not open info.json")
			os.Exit(-1)
		}
		err = json.Unmarshal(inb, &infoStruct)
		if err != nil {
			fmt.Println("Error: could not parse info.json")
			os.Exit(-1)
		}
	}

	var (
		year  = infoStruct.Year
		day   = infoStruct.Day
		title = infoStruct.Title
	)

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

	runTests(infoStruct)

	fmt.Println("Answers")
	fmt.Fprintf(color.Output, "Part %s: %s\n", color.BlueString("1"), color.BlueString(strconv.Itoa(challenge.PartOne(challengeInput))))
	fmt.Fprintf(color.Output, "Part %s: %s\n", color.BlueString("2"), color.BlueString(strconv.Itoa(challenge.PartTwo(challengeInput))))

}

type tc struct {
	Input    string `json:"input"`
	Expected int    `json:"expected"`
}

type info struct {
	Year      string `json:"year"`
	Day       string `json:"day"`
	Title     string `json:"title"`
	TestCases struct {
		One []tc `json:"one"`
		Two []tc `json:"two"`
	} `json:"testCases"`
}

func runTests(infoStruct info) {

	if len(infoStruct.TestCases.One) == 0 && len(infoStruct.TestCases.Two) == 0 {
		fmt.Println("Info: no test cases specified. Skipping tests")
		fmt.Println()
		return
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

	rt(infoStruct.TestCases.One, challenge.PartOne, "1")
	rt(infoStruct.TestCases.Two, challenge.PartTwo, "2")

	fmt.Println()

}
