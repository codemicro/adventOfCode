import sys
from functools import reduce
import math


# time then record dist
Race = tuple[int, int]


def parse(instr: str) -> list[Race]:
    
    times, distances = [[int(y) for y  in x.split(":")[1].split(" ") if y != ""] for x in instr.splitlines()]
    return list(zip(times, distances))

def solve_quadratic(a: int, b: int, c: int) -> list[float]:
    # This doesn't handle less than 2 solutions because we're assuming that AoC
    # isn't (completely) evil
    res = []
    res.append((-b + math.sqrt((b**2) - (4*a*c)))/2*a)
    res.append((-b - math.sqrt((b**2) - (4*a*c)))/2*a)
    return res


def solve_races(races: list[Race]) -> int:
    acc = 1

    for (duration, record) in races:
        roots = solve_quadratic(1, -duration, record)
        a, b = list(sorted(roots))
        a = math.floor(a) + 1
        b = math.ceil(b) - 1
        acc *= b - a + 1

    return acc


def one(instr: str):
    return solve_races(parse(instr))


def two(instr: str):
    races = parse(instr)
    race = tuple(int(reduce(lambda x, y: x + str(y), [race[i] for race in races], "")) for i in range(2))
    return solve_races([race])


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        sys.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))