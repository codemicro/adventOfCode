import json
import platform
import sys
import time

from rich import print

from partOne import partOne
from partTwo import partTwo


force_time = False


def run_and_time(f):
    st = time.time()
    x = f()
    et = time.time()
    return x, et-st


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
            readable_test_num = f"{n}.{i+1}"
            print(f"Running {readable_test_num}...", end="\r")
            
            expectedInt = tc["expected"]

            result, t = run_and_time(lambda: f(str(tc["input"])))

            output_string = f"{readable_test_num} "

            if result == expectedInt:
                output_string += "[green]pass[/green]"
            else:
                output_string += f"[red]fail[/red] (got {result}, expected {expectedInt})"
            
            if t > 15 or force_time:
                output_string += f" in {t} seconds"
            
            print(output_string + " "*12)

    rt(test_cases["one"], partOne, 1)
    rt(test_cases["two"], partTwo, 2)

    print()


if __name__ == "__main__":
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

    if "vis" in sys.argv:
        import visualise

        print("[green]Running visualisation....[/green]")

        visualise.visualise(challenge_input)
        sys.exit()

    if "ft" in sys.argv:
        force_time = True

    run_tests(info["testCases"])

    if "debug" in sys.argv:
        sys.exit()

    print("Answers")
    
    print("Running part 1...", end="\r")
    output_string = "Part 1: "
    x, t = run_and_time(lambda: partOne(challenge_input))
    output_string += str(x)
    if t > 15 or force_time:
        output_string += f" in {t} seconds"
    print(output_string + " "*12)

    print("Running part 2...", end="\r")
    output_string = "Part 2: "
    x, t = run_and_time(lambda: partTwo(challenge_input))
    output_string += str(x)
    if t > 15 or force_time:
        output_string += f" in {t} seconds"
    print(output_string + " "*12)
