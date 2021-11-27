from common import *


def apply_mask(number: int, mask: str) -> int:
    # There has to be a better way to do this... but oh well
    # it works, after all
    value = number_to_base(number, 2).zfill(len(mask))
    combi = ""
    for (v, m) in zip(value, mask.lower()):
        if m == "x":
            combi += v
        else:
            combi += m
    return int(combi, 2)


def partOne(instr: str) -> int:
    input_instructions = parse(instr)
    memory = {}

    for instruction in input_instructions:
        memory[instruction.address] = apply_mask(instruction.value, instruction.mask)

    sigma = 0
    for key in memory:
        sigma += memory[key]

    return sigma
