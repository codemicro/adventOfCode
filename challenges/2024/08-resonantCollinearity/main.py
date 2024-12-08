import sys
from gridutil import grid, coord
from collections import defaultdict
import itertools
from fractions import Fraction


def parse(instr: str) -> tuple[dict[str, list[coord.Coordinate]], tuple[int, int]]:
    g = grid.parse(instr)
    antenna_by_type = defaultdict(list)
    for key in g:
        if g[key] == ".":
            continue
        antenna_by_type[g[key]].append(key)
    return antenna_by_type, (grid.get_max_x(g), grid.get_max_y(g))


def one(instr: str):
    (antenna_by_type, (max_x, max_y)) = parse(instr)

    pos = set()
    for antenna_type in antenna_by_type:
        for (a, b) in itertools.permutations(antenna_by_type[antenna_type], 2):
            diff = coord.sub(b, a)
            c = coord.add(a, coord.mult(diff, 2))
            if 0 <= c.x <= max_x and 0 <= c.y <= max_y:
                pos.add(c)

    return len(pos)


def two(instr: str):
    (antenna_by_type, (max_x, max_y)) = parse(instr)

    pos = set()
    for antenna_type in antenna_by_type:
        for (a, b) in itertools.permutations(antenna_by_type[antenna_type], 2):
            if (
                a.x > b.x
            ):  # filter out (most) duplicate pairs eg ((1, 2), (2, 1)) will only be calculated as ((2, 1), (1, 2)) will be filtered. This also prevents diff.x from being negative (useful for the mod operation)
                continue

            diff = coord.sub(b, a)

            m = Fraction(
                diff.y, diff.x
            )  # equiv of diff.y / diff.x but without the 26.9999999999996 issue
            c = a.y - (m * a.x)

            x_cursor = a.x % diff.x
            y_cursor = int((x_cursor * m) + c)
            while x_cursor <= max_x:
                if 0 <= y_cursor <= max_y:
                    pos.add((x_cursor, y_cursor))
                x_cursor += diff.x
                y_cursor += diff.y

    return len(pos)


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
