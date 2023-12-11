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


def print_coord_grid(universe: Universe):
    n_x = max(map(lambda x: x[0], universe.keys())) + 1
    n_y = max(map(lambda x: x[1], universe.keys())) + 1

    for y in range(n_y):
        for x in range(n_x):
            _debug(universe.get((x, y), "."), end="")
        _debug()


def get_universe_x_size(universe: Universe):
    return max(map(lambda x: x[0], universe.keys())) + 1


def get_universe_y_size(universe: Universe):
    return max(map(lambda x: x[1], universe.keys())) + 1


def expand_universe(universe: Universe, n: int):
    n_x = get_universe_x_size(universe)
    n_y = get_universe_y_size(universe)

    expand_rows = []
    expand_cols = []

    for y in reversed(range(n_y)):
        all_are_empty = True
        for x in range(n_x):
            if universe.get((x, y)) is not None:
                all_are_empty = False
                break

        if all_are_empty:
            expand_rows.append(y)

    for x in reversed(range(n_x)):
        all_are_empty = True
        for y in range(n_y):
            if universe.get((x, y)) is not None:
                all_are_empty = False
                break

        if all_are_empty:
            expand_cols.append(x)

    for src_col_x in reversed(sorted(expand_cols)):
        exp = [galaxy for galaxy in universe if galaxy[0] > src_col_x]
        for galaxy in exp:
            (gx, gy) = galaxy
            v = universe[galaxy]
            del universe[galaxy]
            universe[(gx+n, gy)] = v

    for src_row_y in reversed(sorted(expand_rows)):
        exp = [galaxy for galaxy in universe if galaxy[1] > src_row_y]
        for galaxy in exp:
            (gx, gy) = galaxy
            v = universe[galaxy]
            del universe[galaxy]
            universe[(gx, gy+n)] = v


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