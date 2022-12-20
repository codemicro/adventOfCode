from typing import *
from aocpy import BaseChallenge
from dataclasses import dataclass


@dataclass
class PositionedInteger:
    value: int
    position: int


def parse(instr: str) -> List[PositionedInteger]:
    return [
        PositionedInteger(int(x), i) for i, x in enumerate(instr.strip().splitlines())
    ]


def calc_new_ordinate(o: int, max_ord: int) -> int:
    if o == 0:
        o = max_ord
    else:
        o = o % max_ord
    return o


def mix(inp: List[PositionedInteger]):
    max_ord = len(inp) - 1

    for i in range(len(inp)):
        pos = 0
        n: Optional[PositionedInteger] = None
        while True:
            if inp[pos].position == i:
                n = inp[pos]
                break
            pos += 1

        if n.value == 0:
            continue

        new_pos = calc_new_ordinate(pos + n.value, max_ord)

        _ = inp.pop(pos)
        inp.insert(new_pos, n)


def calc_answer(inp: List[PositionedInteger]) -> int:
    sigma = 0

    for i in range(len(inp)):
        if inp[i].value == 0:
            break

    for n in [i + 1000, i + 2000, i + 3000]:
        sigma += inp[n % len(inp)].value

    return sigma


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        mix(inp)
        return calc_answer(inp)

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)
        for n in inp:
            n.value *= 811589153

        for _ in range(10):
            mix(inp)

        return calc_answer(inp)
