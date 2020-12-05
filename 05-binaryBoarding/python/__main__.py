import json
import platform
import sys

from rich import print

from partOne import partOne
from partTwo import partTwo

def run_tests(test_cases):
    do_tests = True
    if len(test_cases) == 0:
        do_tests = False
    elif len(test_cases["one"]) == 0 and len(test_cases["two"]) == 0:
        do_tests = False

    if not do_tests:
        print("Info: no test cases specified. Skipping tests\n")
        return

    print("Test cases")

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

if __name__ ==  "__main__":
    try:
        info = open("info.json").read()
    except FileNotFoundError:
        print("Error: could not open info.json")
        sys.exit(-1)

    info = json.loads(info)
    
    year = info["year"]
    day = info["day"]
    title = info["title"]

    print(f"[yellow]AoC {year}[/yellow]: day {day} - {title}")
    print(f"Python {platform.python_version()}\n")

    try:
        challenge_input = open("input.txt").read()
    except FileNotFoundError:
        print("Error: could not open input.txt")
        sys.exit(-1)

    run_tests(info["testCases"])

    print("Answers")
    print("Part 1:", partOne(challenge_input))
    print("Part 2:", partTwo(challenge_input))
