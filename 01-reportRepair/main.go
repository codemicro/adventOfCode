package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	inputBytes, _ := ioutil.ReadFile("input.txt")
	inputSlice := strings.Split(strings.TrimSpace(string(inputBytes)), "\n")

	var values []int
	for _, v := range inputSlice {
		str, _ := strconv.Atoi(v)
		values = append(values, str)
	}

	for _, i := range values {
		for _, v := range values {
			if v+i == 2020 {
				fmt.Println("Part one answer is:", v*i)
			}
		}
	}

	fmt.Println()

	for _, i := range values {
		for _, v := range values {
			for _, x := range values {
				if v+i+x == 2020 {
					fmt.Println("Part two answer is:", v*i*x)
				}
			}
		}
	}

}
