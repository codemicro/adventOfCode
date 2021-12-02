from typing import List
from aocpy import BaseChallenge
from dataclasses import dataclass


FORWARD = "forward"
UP = "up"
DOWN = "down"


@dataclass
class Instruction:
    direction: str
    magnitude: int


def parse(instr: str) -> List[Instruction]:
    o = []
    for line in instr.strip().splitlines():
        direction, magnitude = line.split(" ")
        o.append(
            Instruction(direction, int(magnitude)),
        )
    return o


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        depth = 0
        horizontal = 0

        instructions = parse(instr)
        for instruction in instructions:

            if instruction.direction == FORWARD:
                horizontal += instruction.magnitude
            elif instruction.direction == UP:
                depth -= instruction.magnitude
            elif instruction.direction == DOWN:
                depth += instruction.magnitude
            else:
                raise ValueError(f"unknown direction {instruction.direction}")

        return depth * horizontal

    @staticmethod
    def two(instr: str) -> int:
        depth = 0
        horizontal = 0
        aim = 0

        instructions = parse(instr)
        for instruction in instructions:

            if instruction.direction == FORWARD:
                horizontal += instruction.magnitude
                depth += instruction.magnitude * aim
            elif instruction.direction == UP:
                aim -= instruction.magnitude
            elif instruction.direction == DOWN:
                aim += instruction.magnitude
            else:
                raise ValueError(f"unknown direction {instruction.direction}")

        return depth * horizontal
