from common import *


def partOne(instr: str) -> int:
    rules, _, tickets = parse(instr)
    
    invalid_values, _ = find_invalid(rules, tickets)

    return sum(invalid_values)
