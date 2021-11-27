from common import *
from typing import Dict


def count_for_bag(ruleset: Dict[str, Dict[str, int]], test_cl: str) -> int:
    if len(ruleset[test_cl]) == 0:
        return -1

    count = 0

    for child_colour in ruleset[test_cl]:
        child_bags = count_for_bag(ruleset, child_colour)
        if child_bags == -1:
            v = ruleset[test_cl][child_colour]
        else:
            v = ruleset[test_cl][child_colour] * child_bags
            # The below line includes the number of bags that contain all the children - for
            # example, if you had a bag type that had 6 child bags, and there were 3 of these
            # master bags, the line above would add all the child bags (6*3 of them), and the line
            # below would add the 3 container bags.
            v += ruleset[test_cl][child_colour]
        count += v

    return count


def partTwo(instr: str) -> int:
    rules = parse(instr)
    return count_for_bag(rules, target_colour)
