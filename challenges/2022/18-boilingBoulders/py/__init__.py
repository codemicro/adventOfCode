from typing import *
from aocpy import BaseChallenge, foldl

Coordinate = Tuple[int, int, int]
CubeMap = Dict[Coordinate, bool]


ADJACENT_LOCATIONS = (
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
)


def sum_coordinates(ca: Coordinate, cb: Coordinate) -> Coordinate:
    return tuple(a + b for (a, b) in zip(ca, cb))


def parse(instr: str) -> CubeMap:
    res: CubeMap = {}
    for line in instr.strip().splitlines():
        res[tuple(map(int, line.split(",")))] = False
        
    for coord in res:
        is_completely_surrounded = True
        for modifier in ADJACENT_LOCATIONS:
            combined = sum_coordinates(coord, modifier)
            is_completely_surrounded = is_completely_surrounded and combined in res
        res[coord] = is_completely_surrounded

    return res


def count_exposed_faces(targets: Iterable[Coordinate], all_cubes: CubeMap) -> int:
    n = 0
    for coord in targets:
        for modifier in ADJACENT_LOCATIONS:
            if sum_coordinates(coord, modifier) not in all_cubes:
                n += 1
    return n


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


def is_coord_in_range(c: Coordinate, min_c: Coordinate, max_c: Coordinate) -> bool:
    return foldl(
        lambda x, y: x and y,
        ((a <= b <= c) for (a, b, c) in zip(min_c, c, max_c)),
        True,
    )


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        return count_exposed_faces([p for p in inp if not inp[p]], inp)

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)
        
        min_x, max_x = min_max(c[0] for c in inp)
        min_y, max_y = min_max(c[1] for c in inp)
        min_z, max_z = min_max(c[2] for c in inp)
        min_coord = (min_x - 1, min_y - 1, min_z - 1)
        max_coord = (max_x + 1, max_y + 1, max_z + 1)

        visited: Dict[Coordinate, None] = {}
        touchable_faces = 0
        scan_points = [min_coord]
        while len(scan_points) != 0:
            current = scan_points.pop()
            if current in visited:
                continue
            visited[current] = None

            for modifier in ADJACENT_LOCATIONS:
                combined = sum_coordinates(current, modifier)
                if (not is_coord_in_range(combined, min_coord, max_coord)):
                    continue
                
                if combined in inp:
                    touchable_faces += 1
                else:
                    scan_points.append(combined)

        return touchable_faces
