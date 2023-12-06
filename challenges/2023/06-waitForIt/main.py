import sys
from functools import reduce
import math


# time then record dist
Race = tuple[int, int]


def parse(instr: str) -> list[Race]:
    
    times, distances = [[int(y) for y  in x.split(":")[1].split(" ") if y != ""] for x in instr.splitlines()]
    return list(zip(times, distances))


def solve_races(races: list[Race]) -> int:
    acc = 1

    for (duration, record) in races:
        winning_plays = 0

        for i in range(duration):
            time_used = i
            time_remaining = duration - time_used
            speed = i
            distance_travelled = speed * time_remaining
            if distance_travelled > record:
                winning_plays += 1
        
        acc *= winning_plays

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