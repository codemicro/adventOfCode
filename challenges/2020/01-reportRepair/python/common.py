from typing import List


def parse(instr: str) -> List:
    return [int(x) for x in instr.strip().split("\n")]
