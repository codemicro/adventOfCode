import json
import platform
import sys

from rich import print

from partOne import partOne
from partTwo import partTwo

year = "2020"
day = "2"
title = "Password Philosophy"


def run_tests():
    try:
        test_cases = open("testCases.json").read()
    except FileNotFoundError:
        print("Info: could not open testCases.json. Skipping tests")
        return

    print("Test cases")

    test_cases = json.loads(test_cases)

    def rt(tcs, f, n):
        for i, tc in enumerate(tcs):
            print(f"{n}.{i+1} ", end="")
            expectedInt = tc["expected"]
            result = f(str(tc["input"]))
            if result == expectedInt:
                print("[green]pass[/green]")
            else:
                print(f"[red]fail[/red] (got {result}, expected {expectedInt})")

    rt(test_cases["one"], partOne, 1)
    rt(test_cases["two"], partTwo, 2)

    print()


if __name__ == "__main__":
    print(f"[yellow]AoC {year}[/yellow]: day {day} - {title}")
    print(f"Python {platform.python_version()}\n")

    try:
        challenge_input = open("input.txt").read()
    except FileNotFoundError:
        print("Error: could not open input.txt")
        sys.exit(-1)

    run_tests()

    print("Answers")
    print("Part 1:", partOne(challenge_input))
    print("Part 2:", partTwo(challenge_input))
