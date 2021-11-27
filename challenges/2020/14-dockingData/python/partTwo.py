from common import *
import copy


def get_memory_addresses(value: int, mask: str) -> List[int]:

    value = number_to_base(value, 2).zfill(len(mask))
    combi = []
    for (v, m) in zip(value, mask.lower()):
        if m == "0":
            combi.append(v)
        elif m == "1":
            combi.append("1")
        else:
            combi.append(m)

    mask = combi

    n = mask.count("x")
    # generates sets of ones and zeroes in unique orders for n times
    values = list(itertools.product(*[[0, 1]] * n))

    xns = []

    # Find all floating point iterations
    for val_combo in values:
        msk = copy.copy(mask)
        val_counter = 0
        for i, char in enumerate(msk):
            if char == "x":
                msk[i] = str(val_combo[val_counter])
                val_counter += 1
        xns.append(int("".join(msk), 2))

    return xns


def partTwo(instr: str) -> int:
    input_instructions = parse(instr)
    memory = {}

    for instruction in input_instructions:
        addresses = get_memory_addresses(instruction.address, instruction.mask)
        for address in addresses:
            memory[address] = instruction.value

    sigma = 0
    for key in memory:
        sigma += memory[key]

    return sigma
