from common import *


def partTwo(instr: str) -> int:
    forest = parse(instr)

    tree_product = 1

    offset_pairs = [(3, 1), (1, 1), (5, 1), (7, 1), (1, 2)]

    for i, pair in enumerate(offset_pairs):
        encountered_trees = find_collisions(forest, *pair)
        tree_product *= encountered_trees

    return tree_product
