import time
from typing import Tuple, List, Generator
from aocpy import BaseChallenge
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __init__(self, p: str):
        x, y = p.split(",")
        self.x = int(x)
        self.y = int(y)

    def as_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


Line = Tuple[Point, Point]


def parse(instr: str) -> List[Line]:
    o = []
    for line in instr.strip().splitlines():
        p1, p2 = line.split(" -> ")
        o.append((Point(p1), Point(p2)))
    return o


def remove_diagonal_lines(lines: List[Line]) -> List[Line]:
    return list(
        filter(
            lambda line: line[0].x == line[1].x or line[0].y == line[1].y,
            lines,
        )
    )


def iterate_points(line: Line) -> Generator[Point, None, None]:
    p1, p2 = line
    delta_x = p2.x - p1.x
    delta_y = p2.y - p1.y

    x_step = 0
    y_step = 0

    if delta_x > 0:
        x_step = 1
    elif delta_x < 0:
        x_step = -1

    if delta_y > 0:
        y_step = 1
    elif delta_y < 0:
        y_step = -1

    last_point = p1
    yield p1
    while last_point != p2:
        np = Point(f"{last_point.x+x_step},{last_point.y+y_step}")
        yield np
        last_point = np


def count_overlapping_points(lines: List[Line]) -> int:
    areas = {}
    for line in lines:
        for point in iterate_points(line):
            t = point.as_tuple()
            areas[t] = areas.get(t, 0) + 1

    number_overlaps = 0
    for point in areas:
        if areas[point] > 1:
            number_overlaps += 1

    return number_overlaps


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        lines = parse(instr)
        lines = remove_diagonal_lines(lines)
        return count_overlapping_points(lines)

    @staticmethod
    def two(instr: str) -> int:
        lines = parse(instr)
        return count_overlapping_points(lines)
