from typing import List


def parse(instr: str) -> List[int]:
    return [int(x) for x in instr.strip()]
