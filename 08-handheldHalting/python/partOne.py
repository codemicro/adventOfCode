from common import *


def partOne(instr: str) -> int:
    instructions = parse(instr)

    acc = 0
    pc = 0

    visited = []  # indexes of visited instructions

    while True:

        if pc in visited:
            return acc
        else:
            visited.append(pc)

        cir = instructions[pc]

        if cir.opcode == "jmp":
            pc += cir.operand
        else:
            if cir.opcode == "acc":
                acc += cir.operand
            elif cir.opcode == "nop":
                pass
            pc += 1
