from typing import TypeVar, Callable, Optional

import gridutil.coord as coord

T = TypeVar("T")
Grid = dict[coord.Coordinate, T]


def parse(instr: str, filter_fn: Optional[Callable[[str], bool]] = None) -> Grid:
    if filter_fn is None:
        filter_fn = lambda _: True

    res = {}
    for y, line in enumerate(instr.splitlines()):
        for x, char in enumerate(line):
            if filter_fn(char):
                res[(x, y)] = char

    return res


def _get_max(
    grid: Grid, idx: str, filter_fn: Optional[Callable[[T], bool]] = None
) -> int:
    g = grid
    if filter is not None:
        g = filter(filter_fn, grid)
    return max(map(lambda x: x[idx], g))


def get_max_x(grid: Grid, filter_fn: Optional[Callable[[T], bool]] = None) -> int:
    return _get_max(grid, 0, filter_fn=filter_fn)


def get_max_y(grid: Grid, filter_fn: Optional[Callable[[T], bool]] = None) -> int:
    return _get_max(grid, 1, filter_fn=filter_fn)


def print_grid(grid: Grid, **kwargs):
    for y in range(get_max_y(grid) + 1):
        for x in range(get_max_x(grid) + 1):
            v = grid.get((x, y), " ")
            print(v, end="", **kwargs)
        print(**kwargs)
