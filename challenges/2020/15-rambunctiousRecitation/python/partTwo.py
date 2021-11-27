from common import *


def partTwo(instr: str) -> int:
    x, _ = find_value_n(instr, 30000000)
    return x
