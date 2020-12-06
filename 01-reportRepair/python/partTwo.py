from common import *


def partTwo(instr: str) -> int:
    values = parse(instr)

    for i in values:
        for v in values:
            for x in values:
                if v + i + x == 2020:
                    return v * i * x

    return 0
