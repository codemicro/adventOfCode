from typing import Any, List
from aocpy import BaseChallenge


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        values = parse(instr)

        for i in values:
            for v in values:
                if v + i == 2020:
                    return v * i

        raise ValueError("no macthing combinations")

    @staticmethod
    def two(instr: str) -> Any:
        values = parse(instr)

        for i in values:
            for v in values:
                for x in values:
                    if v + i + x == 2020:
                        return v * i * x
        
        raise ValueError("no matching combinations")


def parse(instr: str) -> List:
    return [int(x) for x in instr.strip().split("\n")]
