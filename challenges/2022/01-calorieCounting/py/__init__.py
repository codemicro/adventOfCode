from typing import *
from aocpy import BaseChallenge


def parse(instr: str) -> List[List[int]]:
    return [map(int, x.split("\n")) for x in instr.strip().split("\n\n")]


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> Any:
        parsed = parse(instr)
        x = [sum(y) for y in parsed]
        return max(x)

    @staticmethod
    def two(instr: str) -> Any:
        parsed = parse(instr)
        x = [sum(y) for y in parsed]
        x = list(sorted(x, reverse=True))
        return sum(x[:3])
