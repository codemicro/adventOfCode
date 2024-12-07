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


def evaluate(ns: list[int], ops: Iterable[str]):
    acc = ns[0]
    for i, (v, op) in enumerate(zip(ns[1:], ops)):
        if op == "*":
            acc *= v
        elif op == "+":
            acc += v
        elif op == "|":
            acc = (acc * (10 ** int(math.log10(v) + 1))) + v
        else:
            raise ValueError(f"unknown operation {op}")
    return acc


def one(instr: str):
    cases = parse(instr)

    cached_ops = {}

    n = 0
    for (target, numbers) in cases:
        num_ops = len(numbers) - 1
        if num_ops not in cached_ops:
            cached_ops[num_ops] = tuple(itertools.product("+*", repeat=num_ops))

        for ops in cached_ops[num_ops]:
            v = evaluate(numbers, ops)
            if v == target:
                n += v
                break

    return n


def two(instr: str):
    cases = parse(instr)

    cached_ops = {}

    n = 0
    for (target, numbers) in cases:
        num_ops = len(numbers) - 1
        if num_ops not in cached_ops:
            cached_ops[num_ops] = tuple(itertools.product("+*|", repeat=num_ops))

        for ops in cached_ops[num_ops]:
            v = evaluate(numbers, ops)
            if v == target:
                n += v
                break

    return n


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
