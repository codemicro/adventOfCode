import sys
from math import prod
import itertools
from typing import Callable, Iterable
import functools


def parse(instr: str) -> list[tuple[str, list[str]]]:
    data = instr.splitlines()
    operations = data[-1]
    data = data[:-1]

    breakpoints = []
    for i, char in enumerate(operations):
        if char != " ":
            breakpoints.append(i)

    res = []
    for (bp_start, bp_end) in itertools.pairwise(breakpoints + [None]):
        acc = []
        for line in data:
            if bp_end is None:
                acc.append(line[bp_start:])
            else:
                acc.append(line[bp_start : bp_end - 1])
        res.append((operations[bp_start], acc))

    return res


def process(instr: str, mapper: Callable[[list[str]], Iterable[int]]) -> int:
    problems = parse(instr)
    n = 0
    for (operation, data) in problems:
        digits = mapper(data)
        match operation:
            case "+":
                n += sum(digits)
            case "*":
                n += prod(digits)
            case _:
                assert False, f"unknown operation {operation}"
    return n


def one(instr: str) -> int:
    return process(instr, functools.partial(map, lambda x: int(x.strip())))


def two(instr: str) -> int:
    return process(instr, lambda y: map(lambda x: int(("".join(x)).strip()), zip(*y)))


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
