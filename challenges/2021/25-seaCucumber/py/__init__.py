from typing import Any, List, Tuple, Dict
from aocpy import BaseChallenge


CUCUMBER_EAST = ">"
CUCUMBER_SOUTH = "v"
EMPTY = "."


Point = Tuple[int, int]
SeaBed = Dict[Point, str]


def parse(instr: str) -> SeaBed:
    lines = instr.strip().splitlines()
    o: SeaBed = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            o[(x, y)] = char
    return o


def iterate_once(sea_bed: SeaBed) -> bool:
    # returns true if moves were made

    moves_made = False

    changes: SeaBed = {}

    def get_point_state(p: Point) -> str:
        # if p in changes:
            # return changes[p]
        return 

    # eastbound
    for point in sea_bed:
        point_content = sea_bed[point]

        if point_content != CUCUMBER_EAST:
            continue

        x, y = point

        next_point = (x + 1, y)
        if next_point not in sea_bed:
            next_point = (0, y)

        if sea_bed[next_point] == EMPTY:
            moves_made = True
            changes[next_point] = point_content
            changes[point] = EMPTY

    for point in changes:
        sea_bed[point] = changes[point]

    changes = {}

    # southbound
    for point in sea_bed:
        point_content = sea_bed[point]

        if point_content != CUCUMBER_SOUTH:
            continue

        x, y = point

        next_point = (x, y + 1)
        if next_point not in sea_bed:
            next_point = (x, 0)

        if sea_bed[next_point] == EMPTY:
            moves_made = True
            changes[next_point] = point_content
            changes[point] = EMPTY

    for point in changes:
        sea_bed[point] = changes[point]

    return moves_made


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        sea_bed = parse(instr)
        i = 1
        while iterate_once(sea_bed):
            i += 1
        return i

    @staticmethod
    def two(instr: str) -> int:
        return -1
