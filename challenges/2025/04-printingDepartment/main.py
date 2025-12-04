import sys
from collections import namedtuple
from itertools import product


Coord = namedtuple("Coord", ["x", "y"])


def parse(instr: str) -> dict[Coord, str]:
    res = {}
    for y, line in enumerate(instr.splitlines()):
        for x, char in enumerate(line):
            res[Coord(x, y)] = char
    return res


def collect_movable(grid: dict[Coord, str]) -> set[Coord]:
    res = set()
    for pos in grid:
        if grid[pos] == "@":
            n = 0
            for (dx, dy) in product((-1, 0, 1), repeat=2):
                if not (dx == 0 and dy == 0):
                    if grid.get((pos.x + dx, pos.y + dy)) == "@":
                        n += 1
            if n < 4:
                res.add(pos)
    return res


def one(instr: str) -> int:
    grid = parse(instr)
    return len(collect_movable(grid))


def two(instr: str) -> int:
    grid = parse(instr)
    n = 0
    change = 1
    while change != 0:
        to_remove = collect_movable(grid)
        change = len(to_remove)
        n += change
        for pos in to_remove:
            grid[pos] = "."
    return n


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        sys.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))
