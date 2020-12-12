from typing import List, Tuple


class Instruction:
    action: str
    magnitude: str
    raw: str

    def __init__(self, instruction:str) -> None:
        self.action = instruction[0].lower()
        self.magnitude = int(instruction[1:])
        self.raw = instruction


def parse(instr: str) -> List[Instruction]:
    return [Instruction(x) for x in instr.strip().split("\n")]


def calculate_direction_deltas(direction:str, amount:int) -> Tuple[int, int]:
    # returns a pair of deltas representing lat,long
    lat_delta = 0
    long_delta = 0

    if direction == "n":
        lat_delta += amount
    elif direction == "s":
        lat_delta -= amount
    
    elif direction == "e":
        long_delta += amount
    elif direction == "w":
        long_delta -= amount

    else:
        raise AssertionError(f"invalid direction '{direction}'")

    return lat_delta, long_delta

