import sys
import gridutil.grid as gu
import gridutil.coord as cu
from collections.abc import Callable
from functools import reduce


def parse(instr: str) -> gu.Grid:
    return gu.parse(instr)


def find_n_end_points(grid: gu.Grid, start_pos: cu.Coordinate, n_steps: int, infinite: bool = False) -> int:
    max_x = gu.get_max_x(grid)
    max_y = gu.get_max_y(grid)

    locations = set([start_pos])
    for _ in range(n_steps):
        new_locations = set([])
        for loc in locations:
            for direction in cu.Direction:
                next_pos = cu.add(loc, direction.delta())
                adjusted_next_pos = next_pos
            
                if infinite:
                    if not (0 < adjusted_next_pos.x < max_x):
                        adjusted_next_pos = cu.Coordinate(abs(adjusted_next_pos.x) % (max_x + 1), adjusted_next_pos.y)
                    
                    if not (0 < adjusted_next_pos.y < max_y):
                        adjusted_next_pos = cu.Coordinate(adjusted_next_pos.x, abs(adjusted_next_pos.y) % (max_y + 1))
                    
                if adjusted_next_pos not in grid or grid[adjusted_next_pos] == "#":
                    continue
                new_locations.add(next_pos)

        locations = new_locations
    return len(locations)


def find_start_point(grid: gu.Grid) -> cu.Coordinate:
    for k in grid:
        if grid[k] == "S":
            return k
    raise ValueError("No start position found")


def one(instr: str):
    grid = parse(instr)
    start_pos = find_start_point(grid)
    res = find_n_end_points(grid, start_pos, 64)
    return res


def two(instr: str):
    grid = parse(instr)
    start_pos = find_start_point(grid)

    TARGET_STEPS = 26501365
    WIDTH = int(gu.get_max_x(grid)) + 1
    a, b = TARGET_STEPS // WIDTH, TARGET_STEPS % WIDTH

    _debug(WIDTH, a, b)

    r = []  
    for i in range(3):
        _debug((WIDTH * i) + b)
        r.append(find_n_end_points(grid, start_pos, (WIDTH * i) + b, infinite=True))
    
    _debug(r)
    x, y, z = r
    return x+a*(y-z+(a-1)*(z-(2*y)+x)//2)


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