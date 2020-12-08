from typing import List


class Instruction:
    opcode: str
    operand: int

    def __init__(self, instr: str) -> None:
        self.opcode, t = instr.split(" ")
        self.operand = int(t)


def parse(instr: str) -> List[Instruction]:
    return [Instruction(x) for x in instr.strip().split("\n")]
