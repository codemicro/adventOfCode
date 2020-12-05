from typing import List

def parse(instr:str) -> List:
    return [x.replace("\n", " ") for x in instr.strip().split("\n\n")]
