from __future__ import annotations
import sys
from typing import *
from aocpy import BaseChallenge, Vector, foldl
import re
from dataclasses import dataclass
import portion as P


@dataclass
class Line:
    m: int
    c: int

    @staticmethod
    def from_points(a: Vector, b: Vector) -> Line:
        calc_m = (b.y - a.y) / (b.x - a.x)
        calc_c = a.y - (calc_m * a.x)
        return Line(int(calc_m), int(calc_c))


parse_re = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def parse(instr: str) -> List[Tuple[Vector, Vector]]:
    res = []
    for line in instr.strip().splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, parse_re.match(line).groups())
        res.append(
            (
                Vector(sensor_x, sensor_y),
                Vector(beacon_x, beacon_y),
            )
        )
    return res


def postprocess(
    inp: List[Tuple[Vector, Vector]]
) -> Tuple[
    Dict[Vector, Tuple[Vector, Vector, Vector, Vector]],
    Dict[Vector, Tuple[Line, Line, Line, Line]],
]:
    # 0 top, 1 left, 2 right, 3 bottom
    sensor_points: Dict[Vector, Tuple[Vector, Vector, Vector, Vector]] = {}
    sensor_lines: Dict[Vector, Tuple[Line, Line, Line, Line]] = {}

    for (sensor, beacon) in inp:
        mh = sensor.manhattan_distance(beacon)
        points = (
            Vector(sensor.x, sensor.y - mh),
            Vector(sensor.x - mh, sensor.y),
            Vector(sensor.x + mh, sensor.y),
            Vector(sensor.x, sensor.y + mh),
        )
        sensor_points[sensor] = points

        lines = (
            Line.from_points(points[1], points[0]),
            Line.from_points(points[3], points[1]),
            Line.from_points(points[2], points[0]),
            Line.from_points(points[2], points[3]),
        )
        sensor_lines[sensor] = lines

    return sensor_points, sensor_lines


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        sensor_points, sensor_lines = postprocess(inp)

        target_line = 10 if len(inp) == 14 else 2000000
        ranges: List[Tuple[int, int]] = []

        for (sensor, _) in inp:
            points = sensor_points[sensor]
            # print("polygon(", (", ".join(map(str, (points[0], points[1], points[3], points[2])))), ")")
            lines = sensor_lines[sensor]
            if points[0].y <= target_line <= points[3].y:
                if target_line == points[1].y:
                    ranges.append((points[2].x, points[1].x))
                elif points[0].y <= target_line < points[1].y:
                    ranges.append(
                        (
                            int((target_line - lines[2].c) / lines[2].m),
                            int((target_line - lines[0].c) / lines[0].m),
                        )
                    )
                else:
                    ranges.append(
                        (
                            int((target_line - lines[3].c) / lines[3].m),
                            int((target_line - lines[1].c) / lines[1].m),
                        )
                    )

        s: Set[int] = set()
        for x in ranges:
            s = s.union(set(range(x[1], x[0] + 1)))

        for (_, beacon) in inp:
            if beacon.y == target_line:
                s.discard(beacon.x)

        return len(s)

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)
        sensor_points, sensor_lines = postprocess(inp)

        max_coord = 20 if len(inp) == 14 else 4000000
        line_ranges: List[P.Interval] = [P.empty() for _ in range(max_coord + 1)]

        for (sensor, _) in inp:
            p0, p1, p2, p3 = sensor_points[sensor]
            l0, l1, l2, l3 = sensor_lines[sensor]

            for y in range(max(p0.y, 0), min(p3.y, max_coord) + 1):
                a: int
                b: int
                if y == sensor.y:
                    a, b = p1.x, p2.x
                elif p0.y <= y < p1.y:
                    a, b = int((y - l0.c) / l0.m), int((y - l2.c) / l2.m)
                else:
                    a, b = int((y - l1.c) / l1.m), int((y - l3.c) / l3.m)

                line_ranges[y] = line_ranges[y] | P.closed(
                    max(a, 0), min(b, max_coord) + 1
                )

        for y in range(len(line_ranges)):
            res = line_ranges[y]
            if not res.atomic:
                return (4000000 * res[0].upper) + y

        return 0
