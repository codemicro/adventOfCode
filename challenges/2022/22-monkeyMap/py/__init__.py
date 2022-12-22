from __future__ import annotations
from typing import *
from aocpy import BaseChallenge, Vector
from enum import Enum
from functools import lru_cache


class CellState(Enum):
    WALL = "#"
    OPEN = "."


class Direction(Enum):
    UP = 3
    RIGHT = 0
    DOWN = 1
    LEFT = 2

    def rotate(self, rot_dir: str) -> Direction:
        n = self.value
        n += -1 if rot_dir == "L" else 1

        if n < 0:
            n = 3
        if n >= 4:
            n = 0

        return Direction(n)

    @property
    def delta(self) -> Tuple[int, int]:
        if self.value == self.UP.value:
            return (0, -1)
        elif self.value == self.LEFT.value:
            return (-1, 0)
        elif self.value == self.DOWN.value:
            return (0, 1)
        elif self.value == self.RIGHT.value:
            return (1, 0)
        else:
            raise ValueError(f"unknown direction {self.value}")


Map = Dict[Vector, CellState]


def parse_path(path: str) -> List[Union[str, int]]:
    res_path = []
    acc = ""
    for i, char in enumerate(path):
        acc += char
        if i + 1 < len(path):
            if (not path[i + 1].isdigit()) and char.isdigit():
                res_path.append(int(acc))
                acc = ""
            if path[i + 1].isdigit() and (not char.isdigit()):
                res_path.append(acc)
                acc = ""
    res_path.append(int(acc) if acc.isdigit() else acc)

    return res_path


def parse(instr: str) -> Tuple[Map, List[Union[str, int]]]:
    (raw_map_lines, path) = instr.split("\n\n")
    map_lines = raw_map_lines.rstrip().splitlines()

    monkey_map: Map = {}
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char != " ":
                monkey_map[Vector(x + 1, y + 1)] = CellState(char)

    return monkey_map, parse_path(path.strip())


def min_max(x: Iterable[int]) -> Tuple[int, int]:
    mini, maxi = None, 0

    for item in x:
        if item > maxi:
            maxi = item
        if mini is None or item < mini:
            mini = item

    if mini is None:
        raise ValueError("empty set")

    return mini, maxi


def calc_answer(pos: Vector, facing: Direction) -> int:
    return (1000 * pos.y) + (4 * pos.x) + facing.value


def build_adjacency_mapping() -> Dict[Vector, Tuple[Vector, Direction]]:
    res: Dict[Vector, Tuple[Vector, Direction]] = {}

    def add(a, di, b, d):
        assert a not in res, a
        res[(a, di)] = (b, d)

    for i in range(50):
        add(
            Vector(51 + i, 1),
            Direction.UP,
            Vector(1, 151 + i),
            Direction.RIGHT,
        )

        add(
            Vector(101 + i, 1),
            Direction.UP,
            Vector(1 + i, 200),
            Direction.UP,
        )

        add(
            Vector(150, 1 + i),
            Direction.RIGHT,
            Vector(100, 150 - i),
            Direction.LEFT,
        )

        add(
            Vector(101 + i, 50),
            Direction.DOWN,
            Vector(100, 51 + i),
            Direction.LEFT,
        )

        add(
            Vector(100, 51 + i),
            Direction.RIGHT,
            Vector(101 + i, 50),
            Direction.UP,
        )

        add(Vector(100, 101 + i), Direction.RIGHT, Vector(150, 50 - i), Direction.LEFT)

        add(Vector(51 + i, 150), Direction.DOWN, Vector(50, 151 + i), Direction.LEFT)

        add(Vector(50, 151 + i), Direction.RIGHT, Vector(51 + i, 150), Direction.UP)

        add(
            Vector(1 + i, 200),
            Direction.DOWN,
            Vector(101 + i, 1),
            Direction.DOWN,
        )

        add(
            Vector(1, 151 + i),
            Direction.LEFT,
            Vector(51 + i, 1),
            Direction.DOWN,
        )

        add(Vector(1, 101 + i), Direction.LEFT, Vector(51, 50 - i), Direction.RIGHT)

        add(Vector(1 + i, 101), Direction.UP, Vector(51, 51 + i), Direction.RIGHT)

        add(
            Vector(51, 51 + i),
            Direction.LEFT,
            Vector(1 + i, 101),
            Direction.DOWN,
        )

        add(
            Vector(51, 1 + i),
            Direction.LEFT,
            Vector(1, 150 - i),
            Direction.RIGHT,
        )

    return res


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        monkey_map, path = parse(instr)

        @lru_cache
        def calc_row_caps(row: int) -> Tuple[int, int]:
            return min_max(q.x for q in monkey_map if q.y == row)

        @lru_cache
        def calc_col_caps(col: int) -> Tuple[int, int]:
            return min_max(q.y for q in monkey_map if q.x == col)

        current_pos = Vector(
            min(
                p.x for p in monkey_map if p.y == 1 and monkey_map[p] == CellState.OPEN
            ),
            1,
        )
        facing = Direction.RIGHT

        for instruction in path:
            if type(instruction) == int:

                for _ in range(instruction):
                    next_pos = current_pos + facing.delta

                    if facing == Direction.DOWN:
                        cc = calc_col_caps(next_pos.x)
                        bound = cc[1]
                        if next_pos.y > bound:
                            next_pos.y = cc[0]
                    elif facing == Direction.UP:
                        cc = calc_col_caps(next_pos.x)
                        bound = cc[0]
                        if next_pos.y < bound:
                            next_pos.y = cc[1]
                    elif facing == Direction.RIGHT:
                        rc = calc_row_caps(next_pos.y)
                        bound = rc[1]
                        if next_pos.x > bound:
                            next_pos.x = rc[0]
                    elif facing == Direction.LEFT:
                        rc = calc_row_caps(next_pos.y)
                        bound = rc[0]
                        if next_pos.x < bound:
                            next_pos.x = rc[1]

                    if monkey_map[next_pos] == CellState.WALL:
                        break

                    current_pos = next_pos

            elif type(instruction) == str:
                facing = facing.rotate(instruction)
            else:
                raise TypeError(f"unknown instruction type {type(instruction)}")

        return calc_answer(current_pos, facing)

    @staticmethod
    def two(instr: str) -> int:
        monkey_map, path = parse(instr)

        adj = build_adjacency_mapping()

        current_pos = Vector(
            min(
                p.x for p in monkey_map if p.y == 1 and monkey_map[p] == CellState.OPEN
            ),
            1,
        )
        facing = Direction.RIGHT

        for instruction in path:
            if type(instruction) == int:

                for _ in range(instruction):
                    next_pos = current_pos + facing.delta
                    next_dir = facing

                    if next_pos not in monkey_map:
                        assert (current_pos, facing) in adj
                        next_pos, next_dir = adj[(current_pos, facing)]

                    if monkey_map[next_pos] == CellState.WALL:
                        break

                    current_pos = next_pos
                    facing = next_dir

            elif type(instruction) == str:
                facing = facing.rotate(instruction)
            else:
                raise TypeError(f"unknown instruction type {type(instruction)}")

        return calc_answer(current_pos, facing)
