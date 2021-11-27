from typing import List

tree_char = "#"


def parse(instr: str) -> List:
    return [[char for char in line] for line in instr.strip().split("\n")]


def find_collisions(forest: list, x_offset: int, y_offset: int) -> int:
    encountered_trees = 0
    x_pointer = 0

    for row in forest[::y_offset]:
        target_index = x_pointer % len(row)
        if row[target_index] == tree_char:
            encountered_trees += 1
        x_pointer += x_offset

    return encountered_trees
