from typing import *
from aocpy import BaseChallenge

from queue import LifoQueue as Stack
from dataclasses import dataclass
import re


@dataclass
class MoveInstruction:
    n: int
    source: int
    destination: int


instruction_regexp = re.compile(r"move (\d+) from (\d+) to (\d+)")


def parse(instr: str) -> Tuple[List[Stack], List[MoveInstruction]]:
    raw_initial_state, raw_instructions = instr.rstrip().split("\n\n")

    state_lines = raw_initial_state.splitlines()
    state_lines = state_lines[:-1]  # the last line only contains digits that
    # we don't need to look at
    state_lines = [[line[i : i + 3] for i in range(0, len(line), 4)] for line in state_lines]

    state: List[Stack] = []
    for _ in range(len(state_lines[0])):
        state.append(Stack())

    for line in state_lines[::-1]:
        for i, item in enumerate(line):
            if item != "   ":
                state[i].put_nowait(item[1])

    instructions: List[MoveInstruction] = []

    for line in raw_instructions.strip().splitlines():
        instructions.append(
            MoveInstruction(*map(int, instruction_regexp.match(line).groups()))
        )

    return state, instructions


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> str:
        state, instructions = parse(instr)

        for instruction in instructions:
            for _ in range(instruction.n):
                x = state[instruction.source - 1].get_nowait()
                state[instruction.destination - 1].put_nowait(x)

        return "".join(crate.get_nowait() for crate in state)

    @staticmethod
    def two(instr: str) -> str:
        state, instructions = parse(instr)

        for instruction in instructions:
            items = []
            for _ in range(instruction.n):
                items.append(state[instruction.source - 1].get_nowait())

            for item in items[::-1]:
                state[instruction.destination - 1].put_nowait(item)

        return "".join(crate.get_nowait() for crate in state)
