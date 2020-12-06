from typing import List


def parse(instr: str) -> List[str]:
    return instr.strip().split("\n\n")
