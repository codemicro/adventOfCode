import sys
import itertools
from typing import Iterable
import math


def parse(instr: str) -> list[tuple[int, list[int]]]:
    res = []
    for line in instr.splitlines():
        spa, spb = line.split(": ")
        res.append(
            (int(spa), list(map(int, spb.split(" ")))),
        )
    return res


def ends_with(x: int, y: int) -> bool:
    ycard = int(math.log10(y)) + 1
    return (x - y) * (10**-ycard) == int(x * (10**-ycard))


def trim_int(x: int, y: int) -> int:
    ycard = int(math.log10(y)) + 1
    return int((x - y) * (10**-ycard))


def solve(target: int, ns: list[int], use_concat: bool = False) -> bool:
    v = ns[-1]
    rest = ns[:-1]

    if len(rest) == 0:
        return target == v

    if target % v == 0:
        # this represents a possible multiplication
        if solve(int(target / v), rest, use_concat):
            return True

    if use_concat and ends_with(target, v):
        # this is a possible concatenation
        if solve(trim_int(target, v), rest, use_concat):
            return True

    # last resort, addition
    return solve(target - v, rest, use_concat)


def one(instr: str):
    cases = parse(instr)
    return itertools.accumulate(
        target if solve(target, numbers, use_concat=False) else 0
        for (target, numbers) in cases
    )


def two(instr: str):
    cases = parse(instr)
    return itertools.accumulate(
        target if solve(target, numbers, use_concat=True) else 0
        for (target, numbers) in cases
    )


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
