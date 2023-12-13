from typing import TypeVar, Callable, Optional

T = TypeVar("T")

Coordinate = tuple[int, int]
Grid = dict[Coordinate, T]


def add_coords(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def parse(instr: str, filter_fn: Optional[Callable[[str], bool]] = None) -> Grid:
    if filter is None:
        filter = lambda _: True

    res = {}
    for y, line in enumerate(instr.splitlines()):
        for x, char in enumerate(line):
            if filter_fn(char):
                res[(x, y)] = char

    return res


def _get_max(grid: Grid, idx: str, filter_fn: Optional[Callable[[T], bool]] = None) -> int:
    g = grid
    if filter is not None:
        g = filter(filter_fn, grid)
    return max(map(lambda x: x[idx], g)) 


def get_max_x(grid: Grid, filter_fn: Optional[Callable[[T], bool]] = None) -> int:
    return _get_max(grid, 0, filter_fn=filter_fn)


def get_max_y(grid: Grid, filter_fn: Optional[Callable[[T], bool]] = None) -> int:
    return _get_max(grid, 1, filter_fn=filter_fn)
