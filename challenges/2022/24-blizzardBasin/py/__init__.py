from typing import *
from dataclasses import dataclass
from aocpy import BaseChallenge, Vector
from enum import Enum


class CellState(Enum):
    WALL = "#"
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def delta(self) -> Tuple[int, int]:
        if self == CellState.WALL:
            raise ValueError("cannot get delta of a wall")
        elif self == CellState.UP:
            return (0, -1)
        elif self == CellState.DOWN:
            return (0, 1)
        elif self == CellState.LEFT:
            return (-1, 0)
        elif self == CellState.RIGHT:
            return (1, 0)
        else:
            raise ValueError(f"unknown CellState {self}")


@dataclass
class Valley:
    positions: Dict[Vector, List[CellState]]
    width: int
    height: int
    start: Vector
    end: Vector

    def tick(self):
        old_valley = self.positions
        self.positions = {}

        for cell in old_valley:
            if old_valley[cell][0] == CellState.WALL:
                self.positions[cell] = [CellState.WALL]
                continue

            for blizzard in old_valley[cell]:
                next_pos = cell + blizzard.delta()
                nx = old_valley.get(next_pos, [])
                if len(nx) != 0 and nx[0] == CellState.WALL:
                    if blizzard == CellState.DOWN:
                        next_pos = Vector(cell.x, 1)
                    elif blizzard == CellState.UP:
                        next_pos = Vector(cell.x, self.height - 2)
                    elif blizzard == CellState.LEFT:
                        next_pos = Vector(self.width - 2, cell.y)
                    elif blizzard == CellState.RIGHT:
                        next_pos = Vector(1, cell.y)
                    else:
                        raise ValueError(f"unexpected cell state {blizzard} at {cell=}")
                b = self.positions.get(next_pos, [])
                b.append(blizzard)
                self.positions[next_pos] = b

    def __repr__(self) -> str:
        res = ""
        for y in range(self.height):
            for x in range(self.width):
                pos = self.positions.get(Vector(x, y))
                res += (
                    "."
                    if pos is None
                    else pos[0].value
                    if len(pos) == 1
                    else str(len(pos))
                )
            res += "\n"

        return res[:-1]


def parse(instr: str) -> Valley:
    res: Dict[Vector, List[CellState]] = {}

    start: Optional[Vector] = None
    end: Optional[Vector] = None

    split_lines = instr.strip().splitlines()

    for y, line in enumerate(split_lines):
        for x, char in enumerate(line):
            if char == ".":
                if y == 0:
                    start = Vector(x, y)
                    # res[start] = [CellState.WALL]
                elif y == len(split_lines) - 1:
                    end = Vector(x, y)
            else:
                res[Vector(x, y)] = [CellState(char)]

    assert start is not None
    assert end is not None

    return Valley(res, len(split_lines[0]), len(split_lines), start, end)


def quickest_time(valley: Valley, start: Vector, end: Vector, time: int = 1) -> int:
    states: Dict[Vector, None] = {start: None}
    while True:
        valley.tick()

        for cell in list(states.keys()):

            adjacent = list(
                filter(
                    lambda x: 0 <= x.x <= valley.width and 0 <= x.y <= valley.height,
                    map(lambda x: cell + x, ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0))),
                )
            )

            for j in reversed(range(len(adjacent))):
                pos = adjacent[j]
                if pos in valley.positions:
                    _ = adjacent.pop(j)

            del states[cell]

            for item in adjacent:
                states[item] = None

        if end in states:
            break

        time += 1

    return time


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        valley = parse(instr)
        return quickest_time(valley, valley.start, valley.end)

    @staticmethod
    def two(instr: str) -> int:
        valley = parse(instr)
        a = quickest_time(valley, valley.start, valley.end)
        b = quickest_time(valley, valley.end, valley.start, time=a + 1)
        c = quickest_time(valley, valley.start, valley.end, time=b + 1)
        return c
