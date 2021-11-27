from common import *
from typing import Dict


def check_bag(ruleset: Dict[str, Dict[str, int]], test_cl: str, target_cl: str) -> bool:
    if (
        target_cl in ruleset[test_cl]
    ):  # bag colour can directly contain the target colour
        return True

    for child_colours in ruleset[test_cl]:
        if check_bag(ruleset, child_colours, target_cl):
            return True

    return False


def partOne(instr: str) -> int:
    rules = parse(instr)

    can_contain_target = 0

    for bag_colour in rules:
        if bag_colour != target_colour:
            if check_bag(rules, bag_colour, target_colour):
                can_contain_target += 1

    return can_contain_target
