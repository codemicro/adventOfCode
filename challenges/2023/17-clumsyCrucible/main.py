import sys
import gridutil.grid as gu
import gridutil.coord as cu


def parse(instr: str) -> gu.Grid:
    g = gu.parse(instr)
    return {k: int(g[k]) for k in g}


def get_shortest_path(grid: gu.Grid, start: cu.Coordinate, end: cu.Coordinate) -> list[cu.Coordinate]:
    d = {start: (0, 0, cu.Direction.Right)}
    p = {}
    f = {}

    while end not in d:
        w = min(filter(lambda x: x[0] not in f, d.items()), key=lambda x: x[1][0])[0]
        f[w] = None

        dist_w, prev_steps, prev_direction = d[w]

        for direction in cu.Direction:
            if (direction == prev_direction and prev_steps == 3) or direction == prev_direction.opposite():
                continue
            u = cu.add(w, direction.delta())
            if u not in grid:
                continue

            if u not in d or dist_w + grid[u] < d[u][0]:
                d[u] = (dist_w + grid[u], prev_steps + 1 if direction == prev_direction else 1, direction)
                p[u] = w

                if u == end:
                    break

        # raise SystemExit(14)

    res = [end]
    cursor = p[end]
    while cursor != start:
        res.append(cursor)
        cursor = p[cursor]
    return list(reversed(res))


def one(instr: str):
    grid = parse(instr)
    end = (gu.get_max_x(grid), gu.get_max_y(grid))
    path = get_shortest_path(grid, (0, 0), end)

    gu.print_grid(grid, file=sys.stderr)
    _debug()

    g = grid.copy()
    for p in path:
        g[p] = "█"

    gu.print_grid(g, file=sys.stderr)

    acc = 0
    for node in path:
        acc += grid[node]
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