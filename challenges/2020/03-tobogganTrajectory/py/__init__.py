from typing import List
from aocpy import BaseChallenge

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

class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        return find_collisions(parse(instr), 3, 1)

    @staticmethod
    def two(instr: str) -> int:
        forest = parse(instr)

        tree_product = 1

        offset_pairs = [(3, 1), (1, 1), (5, 1), (7, 1), (1, 2)]

        for i, pair in enumerate(offset_pairs):
            encountered_trees = find_collisions(forest, *pair)
            tree_product *= encountered_trees

        return tree_product
