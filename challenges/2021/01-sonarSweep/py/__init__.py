from typing import List, Any
from aocpy import BaseChallenge


def parse(instr: str) -> List[int]:
    return [int(x) for x in instr.splitlines() if x != ""]


def count_increases(data: List[int]) -> int:
    c = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            c += 1
    return c


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        data = parse(instr)
        return count_increases(data)

    @staticmethod
    def two(instr: str) -> int:
        data = parse(instr)
        sums = [sum(data[i : i + 3]) for i in range(len(data) - 2)]
        return count_increases(sums)
