import sys
import time


Coordinate = tuple[int, int]


def parse(instr: str) -> tuple[dict[Coordinate, str], Coordinate]:
    s_loc = None
    res = {}

    for y, line in enumerate(instr.splitlines()):
        for x, char in enumerate(line):
            coord = (x, y)
            
            if char == "S":
                s_loc = coord
            
            res[coord] = char

    assert s_loc is not None
    return res, s_loc


acceptable_moves = {
    "-": {
        (-1, 0): ["L", "F", "-"],
        (1, 0): ["7", "J", "-"],
    },
    "|": {
        (0, -1): ["7", "F", "|"],
        (0, 1): ["J", "L", "|"],
    },
}

acceptable_moves["L"] = {
    (c := (0, -1)): acceptable_moves["|"][c],
    (c := (1, 0)): acceptable_moves["-"][c],
}

acceptable_moves["J"] = {
    (c := (0, -1)): acceptable_moves["|"][c],
    (c := (-1, 0)): acceptable_moves["-"][c],
}

acceptable_moves["F"] = {
    (c := (0, 1)): acceptable_moves["|"][c],
    (c := (1, 0)): acceptable_moves["-"][c],
}

acceptable_moves["7"] = {
    (c := (0, 1)): acceptable_moves["|"][c],
    (c := (-1, 0)): acceptable_moves["-"][c],
}

acceptable_moves["S"] = {
    **acceptable_moves["|"], **acceptable_moves["-"]
}


def apply_coord_delta(a: Coordinate, b: Coordinate) -> Coordinate:
    aa, ab = a
    ba, bb = b
    return aa + ba, ab + bb


def check_coord(grid: dict[Coordinate, str], coord: Coordinate, vals: list[str]) -> bool:
    v = grid.get(coord)
    if v is None:
        return False

    if v in vals:
        return True

    return False


def get_loop_boundary(grid: dict[Coordinate, str], start: Coordinate) -> dict[Coordinate, int]:
    visited = {start: 0}
    frontier = [start]

    while frontier:
        coord = frontier.pop(0)
        char = grid[coord]
        
        for c in acceptable_moves.get(char, {}):
            c_must_be = acceptable_moves[char][c]
            c = apply_coord_delta(coord, c)
            if c not in grid or c in visited:
                continue
            if check_coord(grid, c, c_must_be):
                frontier.append(c)
                visited[c] = visited[coord] + 1

    return visited


def one(instr: str):
    loop_boundary = get_loop_boundary(*parse(instr))
    return max(loop_boundary.values())


def area(p):
    # https://stackoverflow.com/a/451482
    # HMM. I BARELY UNDERSTAND THIS.
    return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in zip(p, p[1:] + [p[0]])))


def two(instr: str):
    grid, start_coord = parse(instr)
    loop_boundary = get_loop_boundary(grid, start_coord)

    # This hilarious thing turns the loop boundary (dict of points with their
    # distances away from the origin) and orders them into a contiguous
    # sequence of points that represents the geometry of the shape.

    cands = {}

    for key in loop_boundary:
        cands[loop_boundary[key]] = cands.get(loop_boundary[key], []) + [key]

    keys = cands.keys()
    res = []

    for key in sorted(keys):
        res.append(cands[key][0])

    for key in reversed(sorted(keys)):
        if len(cands[key]) < 2:
            continue
        res.append(cands[key][1])

    # The area includes the size of the line itself, which we don't want. And
    # an extra one that I don't understand the source of.

    return int(area(res) - max(loop_boundary.values()) + 1)


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