from typing import Dict, Tuple, List
from aocpy import BaseChallenge

Point = Tuple[int, int]
Cave = Dict[Point, int]

def parse(instr: str) -> Cave:
    # I would be lying if I said I didn't copy this from day 9
    o = {}
    for y, line in enumerate(instr.strip().splitlines()):
        for x, digit in enumerate(line):
            o[(x, y)] = int(digit)
    return o

def print_cave(cave: Cave):
    max_x = max(x for x, y in cave)
    max_y = max(y for x, y in cave)
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(cave[(x, y)], end="")
        print(flush=True)
    print()


def get_adjacent_points(point: Point) -> List[Point]:
    x, y = point
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]


def iterate(cave: Cave) -> Tuple[Cave, int, bool]:
    
    for point in cave:
        cave[point] = cave[point] + 1

    updates = {}
    has_flashed = []

    def handle_nine(point: Point):
        updates[point] = 0
        has_flashed.append(point)
        for adjacent in get_adjacent_points(point):
            if adjacent not in cave:
                continue
            
            previous_value = cave[adjacent]
            if adjacent in updates:
                previous_value = updates[adjacent]

            updates[adjacent] = previous_value + 1

            if previous_value + 1 > 9 and adjacent not in has_flashed:
                handle_nine(adjacent)

    for point in cave:
        if cave[point] > 9:
            if point not in has_flashed:
                handle_nine(point)

    for point in updates:
        cave[point] = updates[point]

    for point in has_flashed:
        cave[point] = 0

    return cave, len(has_flashed), len(has_flashed) == len(cave)


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        cave = parse(instr)
        sigma = 0
        for _ in range(100):
            c, n, _ = iterate(cave)
            cave = c
            sigma += n
        return sigma

    @staticmethod
    def two(instr: str) -> int:
        cave = parse(instr)
        i = 0
        while True:
            i += 1
            c, _, all_flashed = iterate(cave)
            if all_flashed:
                break
            cave = c
        return i
