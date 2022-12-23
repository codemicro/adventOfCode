from __future__ import annotations
from typing import *
from aocpy import BaseChallenge, Vector, min_max
from enum import Enum


class CellState(Enum):
    OCCUPIED = "#"
    EMPTY = "."


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


ADJACENT_POSITIONS = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
]


CHECK_POSITIONS = {
    Direction.NORTH.value: [Direction.NORTH.value, (1, -1), (-1, -1)],
    Direction.EAST.value: [Direction.EAST.value, (1, 1), (1, -1)],
    Direction.SOUTH.value: [Direction.SOUTH.value, (1, 1), (-1, 1)],
    Direction.WEST.value: [Direction.WEST.value, (-1, 1), (-1, -1)],
}

Crater = Dict[Vector, CellState]


def parse(instr: str) -> Crater:
    res: Crater = {}

    for y, line in enumerate(instr.strip().splitlines()):
        for x, char in enumerate(line):
            if char == CellState.OCCUPIED.value:
                res[Vector(x, y)] = CellState.OCCUPIED

    return res


def step(state: Crater, directions: List[Tuple[int, int]]) -> bool:
    next_moves: Dict[Vector, List[Vector]] = {}

    for elf in state:
        for direction in directions:

            has_any_adjacent = False
            for adj_pos in ADJACENT_POSITIONS:
                if elf + adj_pos in state:
                    has_any_adjacent = True
                    break

            if not has_any_adjacent:
                break

            is_avail = True
            for check_pos in CHECK_POSITIONS[direction.value]:
                if elf + check_pos in state:
                    is_avail = False
                    break

            if is_avail:
                pos = elf + direction.value
                x = next_moves.get(pos, [])
                x.append(elf)
                next_moves[pos] = x
                break

    for target_pos in next_moves:
        if len(next_moves[target_pos]) != 1:
            continue

        state[target_pos] = CellState.OCCUPIED
        del state[next_moves[target_pos][0]]

    return len(next_moves) != 0


def print_crater(cr: Crater):
    for y in range(-2, -2 + 12):
        for x in range(-3, -3 + 14):
            print(cr[(x, y)].value if (x, y) in cr else ".", end="")
        print()

    print("________________", flush=True)


def calc_open_area(state: Crater) -> int:
    min_x, max_x = min_max(p.x for p in state)
    min_y, max_y = min_max(p.y for p in state)

    max_x += 1
    max_y += 1

    return ((max_x - min_x) * (max_y - min_y)) - len(state)


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)

        directions = [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.WEST,
            Direction.EAST,
        ]

        for _ in range(10):
            step(inp, directions)
            directions.append(directions.pop(0))

        return calc_open_area(inp)

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)

        directions = [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.WEST,
            Direction.EAST,
        ]

        n = 0
        while True:
            did_something_move = step(inp, directions)
            n += 1
            if not did_something_move:
                break
            directions.append(directions.pop(0))

        return n
