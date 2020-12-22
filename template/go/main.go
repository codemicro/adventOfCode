package main

import (
	"adventOfCode/template/go/challenge"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"runtime"
	"strconv"
	"time"

	"github.com/fatih/color"
)

var forceTime bool

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

	for _, v := range os.Args[1:] {
		if v == "ft" {
			forceTime = true
		}
	}

	runTests(infoStruct)

	fmt.Println("Answers")

	fmt.Printf("Running part %s...\r", color.BlueString("1"))
	outputString := fmt.Sprintf("Part %s: ", color.BlueString("1"))
	x, t := runAndTime(func() int { return challenge.PartOne(challengeInput) })
	outputString += color.BlueString(strconv.Itoa(x))
	if t > 15 || forceTime {
		outputString += fmt.Sprintf(" in %s seconds", color.BlueString(fmt.Sprintf("%.8f", t)))
	}
	for i := 0; i < 12; i += 1 {
		outputString += " "
	}
	outputString += "\n"
	fmt.Fprint(color.Output, outputString)

	fmt.Printf("Running part %s...\r", color.BlueString("2"))
	outputString = fmt.Sprintf("Part %s: ", color.BlueString("2"))
	x, t = runAndTime(func() int { return challenge.PartTwo(challengeInput) })
	outputString += color.BlueString(strconv.Itoa(x))
	if t > 15 || forceTime {
		outputString += fmt.Sprintf(" in %s seconds", color.BlueString(fmt.Sprintf("%.8f", t)))
	}
	for i := 0; i < 12; i += 1 {
		outputString += " "
	}
	outputString += "\n"
	fmt.Fprint(color.Output, outputString)

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
			readable_test_num := color.BlueString(n + "." + strconv.Itoa(i+1))
			fmt.Fprintf(color.Output, "Running %s...\r", readable_test_num)

			outputString := readable_test_num + " "

			result, t := runAndTime(func() int { return f(tc.Input) })

			if result == tc.Expected {
				outputString += color.GreenString("pass")
			} else {
				outputString += fmt.Sprintf("%s (got %s, expected %s)", color.RedString("fail"), color.BlueString(strconv.Itoa(result)), color.BlueString(strconv.Itoa(tc.Expected)))
			}

			if t > 15 || forceTime {
				outputString += fmt.Sprintf(" in %s seconds", color.BlueString(fmt.Sprintf("%.8f", t)))
			}

			for i := 0; i < 12; i += 1 {
				outputString += " "
			}
			outputString += "\n"

			fmt.Fprint(color.Output, outputString)
		}
	}

	rt(infoStruct.TestCases.One, challenge.PartOne, "1")
	rt(infoStruct.TestCases.Two, challenge.PartTwo, "2")

	fmt.Println()

}

func runAndTime(f func() int) (int, float64) {
	st := time.Now()
	x := f()
	et := time.Now()
	return x, et.Sub(st).Seconds()
}
