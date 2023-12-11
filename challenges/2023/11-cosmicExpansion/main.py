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
            res[(x, y)] = char
    return res


def print_coord_grid(universe: Universe):
    n_x = max(map(lambda x: x[0], universe.keys())) + 1
    n_y = max(map(lambda x: x[1], universe.keys())) + 1

    for y in range(n_y):
        for x in range(n_x):
            _debug(universe[(x, y)], end="")
        _debug()


def get_universe_x_size(universe: Universe):
    return max(map(lambda x: x[0], universe.keys())) + 1


def get_universe_y_size(universe: Universe):
    return max(map(lambda x: x[1], universe.keys())) + 1


def expand_universe(universe: Universe):
    n_x = get_universe_x_size(universe)
    n_y = get_universe_y_size(universe)

    expand_rows = []
    expand_cols = []

    for y in reversed(range(n_y)):
        all_are_empty = True
        for x in range(n_x):
            if universe[(x, y)] != ".":
                all_are_empty = False
                break

        if all_are_empty:
            expand_rows.append(y)

    for x in reversed(range(n_x)):
        all_are_empty = True
        for y in range(n_y):
            if universe[(x, y)] != ".":
                all_are_empty = False
                break

        if all_are_empty:
            expand_cols.append(x)

    for src_col_x in reversed(sorted(expand_cols)):
        for x in reversed(range(src_col_x + 1, get_universe_x_size(universe) + 1)): # we don't want to touch the starting col but we do want to overflow by one
            for y in range(n_y):
                universe[(x, y)] = universe[(x - 1, y)]

    n_x = get_universe_x_size(universe)

    for src_row_y in reversed(sorted(expand_rows)):
        for y in reversed(range(src_row_y + 1, get_universe_y_size(universe) + 1)): # we don't want to touch the starting col but we do want to overflow by one
            for x in range(n_x):
                universe[(x, y)] = universe[(x, y - 1)]


# def heuristic(a: Coordinate, b: Coordinate) -> float:
#     (c, d) = a
#     (e, f) = b
#     return math.sqrt((e - c) ** 2 + (f - d) ** 2)


# def get_shortest_path_len(universe: Universe, start: Coordinate, end: Coordinate) -> int:
#     d = {start: 0}
#     h = {start: 0}
#     p = {}
#     f = {}

#     while end not in d:
#         w = min(filter(lambda x: x[0] not in f, h.items()), key=lambda x: x[1])[0]
#         f[w] = None

#         for cardinal_dir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
#             u = apply_coord_delta(w, cardinal_dir)
#             if u not in universe:
#                 continue

#             if u not in d or h[w] + 1 < h[u]:
#                 d[u] = d[w] + 1
#                 h[u] = heuristic(w, u)
#                 p[u] = w

#                 if u == end:
#                     break

#     return d[end]

def get_shortest_path_len(start: Coordinate, end: Coordinate) -> int:
    (xa, ya) = start
    (xb, yb) = end
    return abs(xb - xa) + abs(yb - ya)


def one(instr: str):
    universe = parse(instr)
    expand_universe(universe)

    galaxies = []
    for y in range(get_universe_y_size(universe)):
        for x in range(get_universe_x_size(universe)):
            if universe[(x, y)] == "#":
                galaxies.append((x, y))

    galaxy_pairs = {}
    for g in galaxies:
        for h in galaxies:
            if h == g or (g, h) in galaxy_pairs or (h, g) in galaxy_pairs:
                continue
            galaxy_pairs[(g, h)] = None
    galaxy_pairs = list(galaxy_pairs.keys())

    acc = 0
    n = len(galaxy_pairs)
    for i, (a, b) in enumerate(galaxy_pairs):
        _debug(f"{i}/{n} - ", end="")
        # h = heuristic(a, b)
        sp = get_shortest_path_len(a, b)
        _debug(h, sp)
        acc += sp
    return acc


def two(instr: str):
    return


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