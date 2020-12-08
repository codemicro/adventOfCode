import copy
from typing import List, Tuple

from common import *


def execute(instructions: List[Instruction]) -> Tuple[bool, int]:
    # Returning false means a loop occured. Returning true means no loop occured.
    # The value of the accumulator is always returned

    acc = 0
    pc = 0

    visited = []  # indexes of visited instructions

    while True:

        if pc >= len(instructions):
            # Clean exit
            return True, acc

        if pc in visited:
            # Loop is going to occur at some point
            return False, acc
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


def partTwo(instr: str) -> int:
    master_instructions = parse(instr)

    # I imagine there's probably a smart way to do this... but I'm going to bruteforce it haha

    # Build list of locations of instructions to be switched
    switch_set_locations = []
    for idx, instruction in enumerate(master_instructions):
        if instruction.opcode in ["jmp", "nop"]:
            switch_set_locations.append(idx)

    for slc in switch_set_locations:
        instructions = copy.deepcopy(master_instructions)
        
        # Switch instruction
        oldval = instructions[slc].opcode
        instructions[slc].opcode = "jmp" if oldval == "nop" else "nop"

        # Execute
        clean_exit, acc = execute(instructions)
        if clean_exit:
            break

    return acc
