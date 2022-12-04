from typing import *
from aocpy import BaseChallenge
import re


ElfTaskRange = Tuple[int, int]
ElfPair = Tuple[ElfTaskRange, ElfTaskRange]

parse_re = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def parse(instr: str) -> List[ElfPair]:
    x = instr.strip().splitlines()
    for i, ep in enumerate(x):
        a, b, c, d = map(int, parse_re.match(ep).groups())
        x[i] = ((a, b), (c, d))
    return x


def make_set(tr: ElfTaskRange) -> Set[int]:
    return set(range(tr[0], tr[1] + 1))


def count(inp: List[ElfPair], pred: Callable[[Set[int], Set[int], int], bool]) -> int:
    # pred(first set, second set, length of intersection)

    n = 0
    for pair in inp:
        a = make_set(pair[0])
        b = make_set(pair[1])
        intersection = a.intersection(b)

        if pred(a, b, len(intersection)):
            n += 1

    return n


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        return count(inp, lambda a, b, i: i == len(a) or i == len(b))

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)
        return count(inp, lambda _, __, i: i != 0)
