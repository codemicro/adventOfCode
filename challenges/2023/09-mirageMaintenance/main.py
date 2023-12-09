import sys
from functools import reduce
from typing import Callable


def parse(instr: str) -> list[list[int]]:
    return [[int(x) for x in line.split(" ")] for line in instr.splitlines()]


def get_term(start: list[int], reduction_fn: Callable[[int, list[int]], int]) -> int:
    seqs = [start]
    while not reduce(lambda acc, v: acc and v == 0, seqs[-1], True):
        cs = seqs[-1]
        x = []
        for i in range(len(cs) - 1):
            x.append(cs[i+1] - cs[i])
        seqs.append(x)
    return reduce(reduction_fn, seqs[-2::-1], 0)


def run(instr: str, reduction_fn: Callable[[int, list[int]], int]):
    sequences = parse(instr)
    acc = 0
    for sq in sequences:
        acc += get_term(sq, reduction_fn)
    return acc 


def one(instr: str):
    return run(instr, lambda acc, x: acc + x[-1])


def two(instr: str):
    return run(instr, lambda acc, x: x[0] - acc)


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