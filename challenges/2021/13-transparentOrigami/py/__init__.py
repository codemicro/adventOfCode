import re
from typing import Dict, Tuple, List
from aocpy import BaseChallenge
from dataclasses import dataclass


Point = Tuple[int, int]
Sheet = Dict[Point, bool]


INSTRUCTION_REGEX = re.compile(r"fold along (x|y)=(\d+)")


@dataclass
class Instruction:
    axis: str
    n: int


def parse(instr: str) -> Tuple[Sheet, List[Instruction]]:
    sheetPoints, instructions = instr.strip().split("\n\n")
    
    sheet = {}
    for point in sheetPoints.splitlines():
        x, y = point.split(",")
        sheet[(int(x), int(y))] = True

    ins = []
    for line in instructions.splitlines():
        m = INSTRUCTION_REGEX.match(line)
        ins.append(Instruction(
            m.group(1),
            int(m.group(2)),
        )
        )


    return sheet, ins


def print_sheet(sheet: Sheet):
    max_x = max(x for x, y in sheet)
    max_y = max(y for x, y in sheet)
    lines = []
    for y in range(max_y + 1):
        ll = ""
        for x in range(max_x + 1):
            ll += "██" if sheet.get((x, y), False) else "  "
        lines.append(ll)
    for x in lines:
        print(x, flush=True)


def apply_instruction(sheet: Sheet, instruction: Instruction) -> Sheet:

    # max_val = max((x for x, _ in sheet) if instruction.axis == "x" else (y for _, y in sheet))

    def mod_point(p: Point) -> Point:
        v = p[0]
        if instruction.axis == "y":
            v = p[1]

        if v > instruction.n:
            if instruction.axis == "x":
                return (instruction.n - (p[0] - instruction.n), p[1])
            elif instruction.axis == "y":
                return (p[0], instruction.n - (p[1] - instruction.n))
            raise ValueError(f"unknown axis {instruction.axis}")
        
        return p

    new_sheet = {}
    for point in sheet:
        new_sheet[mod_point(point)] = True

    return new_sheet


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        sheet, instructions = parse(instr)
        sheet = apply_instruction(sheet, instructions[0])
        return sum(sheet.values())

    @staticmethod
    def two(instr: str) -> str:
        sheet, instructions = parse(instr)
        for instruction in instructions:
            sheet = apply_instruction(sheet, instruction)
        print_sheet(sheet)
        return "work it out yourself"
