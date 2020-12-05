from common import *

def partOne(instr:str) -> int:
    values = parse(instr)

    for i in values:
        for v in values:
            if v + i == 2020:
                return v * i

    return 0
