from typing import *
from aocpy import BaseChallenge


def parse(instr: str) -> List[str]:
    return instr.strip().splitlines()


def get_priority(char: str) -> int:
    char = char[0]
    co = ord(char)
    if ord("a") <= co and co <= ord("z"):
        return (co - ord("a")) + 1
    return (co - ord("A")) + 27

class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)

        sigma = 0
        for x in inp:
            assert len(x) % 2 == 0
            l = len(x)//2
            y = set(x[:l]).intersection(x[l:])
            sigma += get_priority(y.pop())

        return sigma

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)
        assert len(inp) % 3 == 0

        sigma = 0
        for i in range(0, len(inp), 3):
            y = set(inp[i])
            y.intersection_update(inp[i+1])
            y.intersection_update(inp[i+2])
            
            sigma += get_priority(y.pop())

        return sigma
