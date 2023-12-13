import sys
import gridutil.grid as gu
from collections import defaultdict
from typing import Optional, Callable, Iterable


def parse(instr: str) -> list[gu.Grid]:
    res = []
    for block in instr.split("\n\n"):
        res.append(gu.parse(block, filter_fn=lambda x: x != "."))
    return res


Acceptor = Callable[[Iterable[int]], bool]


def find_vertical_reflections(
    grid: gu.Grid, make_accept_fn: Callable[[], Acceptor]
) -> set[int]:
    max_x = gu.get_max_x(grid)
    max_y = gu.get_max_y(grid)

    res = set()

    for base_x in range(max_x):
        acceptable = True

        accept_fn = make_accept_fn()

        diff = min(max_x - base_x, base_x + 1)
        range_from = max(0, base_x + 1 - diff)
        range_to = min(max_x, base_x + diff) + 1

        for y in range(max_y + 1):
            dists = defaultdict(lambda: 0)

            for x in range(range_from, range_to):
                if grid.get((x, y)) is None:
                    continue

                if x > base_x:
                    key = x - base_x - 1
                else:
                    key = base_x - x

                dists[key] = dists[key] + 1

            if not accept_fn(dists.values()):
                acceptable = False
                break

        if acceptable:
            res.add(base_x)

    return res


def make_standard_acceptor() -> Acceptor:
    def inner(x: Iterable[int]) -> bool:
        for v in x:
            if v != 2:
                return False
        return True

    return inner


def make_smudge_acceptor() -> Acceptor:
    n = 0

    def inner(x: Iterable[int]) -> bool:
        nonlocal n
        for v in x:
            if v != 2:
                if n == 1:
                    return False
                n += 1
        return True

    return inner


def swap_x_y(grid: gu.Grid) -> gu.Grid:
    res = {}
    for (x, y) in grid:
        res[(y, x)] = grid[(x, y)]
    return res


def set_to_option(x: set[int]) -> Optional[int]:
    assert len(x) <= 1
    if len(x) == 0:
        return None
    return x.pop()


def one(instr: str):
    grids = parse(instr)

    acc = 0

    for grid in grids:
        v = find_vertical_reflections(grid, make_standard_acceptor)
        h = find_vertical_reflections(swap_x_y(grid), make_standard_acceptor)

        if (v := set_to_option(v)) is not None:
            acc += v + 1

        if (h := set_to_option(h)) is not None:
            acc += (h + 1) * 100

    return acc


def two(instr: str):
    grids = parse(instr)

    acc = 0

    for grid in grids:
        v = find_vertical_reflections(
            grid, make_smudge_acceptor
        ) - find_vertical_reflections(grid, make_standard_acceptor)

        sgrid = swap_x_y(grid)
        h = find_vertical_reflections(
            sgrid, make_smudge_acceptor
        ) - find_vertical_reflections(sgrid, make_standard_acceptor)

        if (v := set_to_option(v)) is not None:
            acc += v + 1

        if (h := set_to_option(h)) is not None:
            acc += (h + 1) * 100

    return acc


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
