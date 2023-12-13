package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

func parse(instr string) any {
	return nil
}

func one(instr string) int {
	return -1
}

func two(instr string) int {
	return -1
}

func main() {
	if len(os.Args) < 2 || !(os.Args[1] == "1" || os.Args[1] == "2") {
		debug("Missing day argument")
		os.Exit(1)
	}

	inp, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	inpStr := strings.TrimSpace(string(inp))

	switch os.Args[1] {
	case "1":
		fmt.Println(one(inpStr))
	case "2":
		fmt.Println(two(inpStr))
	}
}

func debug(f string, sub ...any) {
	fmt.Fprintf(os.Stderr, f, sub...)
}
