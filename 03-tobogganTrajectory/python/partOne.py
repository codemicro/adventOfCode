from common import *

def partOne(instr:str) -> int:
    return find_collisions(parse(instr), 3, 1)
