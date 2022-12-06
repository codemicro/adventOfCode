from typing import *
from aocpy import BaseChallenge


def find_unique_sequence(instr: str, length: int) -> int:
    for i in range(len(instr) - length):
        if len(set(instr[i : i + length])) == length:
            return i + length
    raise ValueError("cannot solve")


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        return find_unique_sequence(instr, 4)

    @staticmethod
    def two(instr: str) -> int:
        return find_unique_sequence(instr, 14)
