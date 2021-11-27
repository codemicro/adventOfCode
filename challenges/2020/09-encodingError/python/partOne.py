from typing import Set

from common import *


def has_combinations(options: Set[int], target: int) -> bool:
    # Returns true of the options set has two values that sum to be the target, else returns false

    options = sorted(options)

    l_ptr = 0
    r_ptr = len(options) - 1

    while l_ptr < r_ptr:
        v = options[l_ptr] + options[r_ptr]
        if v == target:
            return True
        elif v < target:
            l_ptr += 1
        else:
            r_ptr -= 1

    return False


def partOne(instr: str) -> int:
    input_list = parse(instr)

    preamble_len = 25
    if len(input_list) < 30:  # This is for tests
        preamble_len = 5

    pointer = preamble_len
    while pointer < len(input_list):
        if not has_combinations(
            set(input_list[pointer - preamble_len : pointer]), input_list[pointer]
        ):
            return input_list[pointer]
        pointer += 1

    return 0
