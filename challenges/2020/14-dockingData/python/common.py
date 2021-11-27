from typing import List, Tuple
import re
import itertools


class Instruction:
    address: int
    value: int
    mask: str

    def __init__(self, instruction: str, mask: str):
        if mask is None:
            raise ValueError(f"bad mask")
        m = re.match(r"mem\[(\d+)\] ?= ?(\d+)", instruction)
        if m is None:
            raise ValueError(f"unable to parse input instruction '{instruction}'")
        self.mask = mask
        self.address = int(m.group(1))
        self.value = int(m.group(2))


def parse(instr: str) -> List[Instruction]:
    retval = []

    current_mask = None
    for line in instr.strip().split("\n"):
        if "mask" in line:
            current_mask = line.split("=")[-1].strip()
        else:
            retval.append(Instruction(line, current_mask))

    return retval


def number_to_base(n: int, b: int) -> str:
    if n == 0:
        return "0"
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return "".join([str(x) for x in digits[::-1]])
