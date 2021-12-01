from typing import List, Any
from aocpy import BaseChallenge


def parse(instr: str) -> List[int]:
    return [int(x) for x in instr.splitlines() if x != ""]


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        data = parse(instr)
        c = 0
        for i in range(1, len(data)):
            if data[i] > data[i-1]:
                c += 1
        return c

    @staticmethod
    def two(instr: str) -> int:
        data = parse(instr)
        c = 0
        sums = [sum(data[i:i+3]) for i in range(len(data)-2)]
        for i in range(1, len(sums)):
            if sums[i] > sums[i-1]:
                c += 1
        return c
