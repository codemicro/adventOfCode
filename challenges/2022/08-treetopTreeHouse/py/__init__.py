from typing import *
from aocpy import BaseChallenge


Coordinate = Tuple[int, int]
Forest = Dict[Coordinate, int]


def parse(instr: str) -> Tuple[Forest, Coordinate]:
    res: Forest = {}

    for x, line in enumerate(instr.strip().splitlines()):
        for y, char in enumerate(line):
            res[(x, y)] = int(char)

    return res, (x, y)


def are_adjacents_lower(forest: Forest, initial_pos: Coordinate, next_pos: Callable[[Coordinate], Coordinate]) -> bool:
    height = forest[initial_pos]
    pos = next_pos(initial_pos)
    while pos in forest:
        if forest[pos] >= height:
            return False
        pos = next_pos(pos)
    return True

def get_viewing_distance(forest: Forest, initial_pos: Coordinate, next_pos: Callable[[Coordinate], Coordinate]) -> int:
    viewing_dist = 0

    height = forest[initial_pos]
    pos = next_pos(initial_pos)
    while pos in forest:
        viewing_dist += 1
        if forest[pos] >= height:
            break
        pos = next_pos(pos)

    return viewing_dist

class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        forest, (max_x, max_y) = parse(instr)
        
        count = 0
        for tree_pos in forest:
            x, y = tree_pos
            if x == 0 or y == 0 or x == max_x or y == max_y:
                count += 1
                continue
            
            # left -x
            if are_adjacents_lower(forest, tree_pos, lambda x: (x[0]-1, x[1])):
                count += 1
                continue
            # right +x
            if are_adjacents_lower(forest, tree_pos, lambda x: (x[0]+1, x[1])):
                count += 1
                continue
            # up -y
            if are_adjacents_lower(forest, tree_pos, lambda x: (x[0], x[1]-1)):
                count += 1
                continue
            # down +y
            if are_adjacents_lower(forest, tree_pos, lambda x: (x[0], x[1]+1)):
                count += 1
                continue

        return count


    @staticmethod
    def two(instr: str) -> int:
        forest, _ = parse(instr)
        
        max_senic = 0
        for tree_pos in forest:
            view_left = get_viewing_distance(forest, tree_pos, lambda x: (x[0]-1, x[1]))
            view_right = get_viewing_distance(forest, tree_pos, lambda x: (x[0]+1, x[1]))
            view_up = get_viewing_distance(forest, tree_pos, lambda x: (x[0], x[1]-1))
            view_down = get_viewing_distance(forest, tree_pos, lambda x: (x[0], x[1]+1))

            senic = view_left * view_right * view_up * view_down
            if senic > max_senic:
                max_senic = senic

        return max_senic
