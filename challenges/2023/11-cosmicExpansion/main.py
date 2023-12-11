import sys
import math


Coordinate = tuple[int, int]
Universe = dict[Coordinate, str]


def apply_coord_delta(a: Coordinate, b: Coordinate) -> Coordinate:
    aa, ab = a
    ba, bb = b
    return aa + ba, ab + bb


def parse(instr: str) -> Universe:
    res = {}
    for y, line in enumerate(instr.splitlines()):
        for x, char in enumerate(line):
            if char != ".":
                res[(x, y)] = char
    return res


def expand_universe(universe: Universe, n: int):
    used_rows = list(map(lambda x: x[1], universe.keys()))
    expand_rows = [i for i in range(max(used_rows)) if i not in used_rows]

    used_cols = list(map(lambda x: x[0], universe.keys()))
    expand_cols = [i for i in range(max(used_cols)) if i not in used_cols]

    for src_col_x in reversed(sorted(expand_cols)):
        exp = [galaxy for galaxy in universe if galaxy[0] > src_col_x]
        for galaxy in exp:
            (gx, gy) = galaxy
            v = universe[galaxy]
            del universe[galaxy]
            universe[(gx + n, gy)] = v

    for src_row_y in reversed(sorted(expand_rows)):
        exp = [galaxy for galaxy in universe if galaxy[1] > src_row_y]
        for galaxy in exp:
            (gx, gy) = galaxy
            v = universe[galaxy]
            del universe[galaxy]
            universe[(gx, gy + n)] = v


def get_shortest_path_len(start: Coordinate, end: Coordinate) -> int:
    (xa, ya) = start
    (xb, yb) = end
    return abs(xb - xa) + abs(yb - ya)


def run(instr: str, expand_to: int) -> int:
    universe = parse(instr)
    expand_universe(universe, expand_to - 1)

    galaxy_pairs = {}
    for g in universe:
        for h in universe:
            if h == g or (g, h) in galaxy_pairs or (h, g) in galaxy_pairs:
                continue
            galaxy_pairs[(g, h)] = None
    galaxy_pairs = list(galaxy_pairs.keys())

    acc = 0
    for (a, b) in galaxy_pairs:
        acc += get_shortest_path_len(a, b)
    return acc


def one(instr: str):
    return run(instr, 2)


def two(instr: str):
    return run(instr, 1_000_000)


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
