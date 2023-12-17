import sys
import gridutil.grid as gu
import gridutil.coord as cu
from collections.abc import Callable, Iterator
from collections import namedtuple
from queue import PriorityQueue


def parse(instr: str) -> gu.Grid:
    g = gu.parse(instr)
    return {k: int(g[k]) for k in g}


State = namedtuple("State", ["pos", "steps_taken", "direction"])


def djikstra(
    start: State,
    end: Callable[[State], bool],
    neighbours: Callable[[State], Iterator[State, None, None]],
    cost: Callable[[State, State], int],
) -> list[State]:
    dq = PriorityQueue()
    dq.put((0, start))
    d = {start: 0}
    p = {}

    endState = None
    while endState is None:
        w = dq.get()[1]

        for u in neighbours(w):
            c = d[w] + cost(w, u)
            if u not in d or c < d[u]:
                d[u] = c
                dq.put((c, u))
                p[u] = w

                if end(u):
                    endState = u
                    break

    res = [endState]
    cursor = p[endState]
    while cursor is not None:
        res.append(cursor)
        cursor = p.get(cursor)
    return list(reversed(res))


def one(instr: str):
    grid = parse(instr)
    end = (gu.get_max_x(grid), gu.get_max_y(grid))

    def neighbours(node: State) -> Iterator[State, None, None]:
        for direction in cu.Direction:
            if (
                direction == node.direction and node.steps_taken == 3
            ) or node.direction == direction.opposite():
                continue

            nc = cu.add(node.pos, direction.delta())
            if nc not in grid:
                continue

            yield State(
                nc,
                (node.steps_taken + 1) if direction == node.direction else 1,
                direction,
            )

    path = djikstra(
        State((0, 0), 0, cu.Direction.Right),
        lambda x: x.pos == end,
        neighbours,
        lambda _, x: grid[x.pos],
    )[1:]

    acc = 0
    for node in path:
        acc += grid[node.pos]
    return acc


def two(instr: str):
    grid = parse(instr)
    end = (gu.get_max_x(grid), gu.get_max_y(grid))

    for x in range(end[0] - 3, end[0]):
        for y in range(end[1] - 3, end[1]):
            del grid[(x, y)]

    def neighbours(node: State) -> Iterator[State, None, None]:
        for direction in cu.Direction:
            if 0 < node.steps_taken < 4 and direction != node.direction:
                continue

            if (
                direction == node.direction and node.steps_taken == 10
            ) or node.direction == direction.opposite():
                continue

            nc = cu.add(node.pos, direction.delta())
            if nc not in grid:
                continue

            yield State(
                nc,
                (node.steps_taken + 1) if direction == node.direction else 1,
                direction,
            )

    path = djikstra(
        State((0, 0), 0, cu.Direction.Right),
        lambda x: x.pos == end,
        neighbours,
        lambda _, x: grid[x.pos],
    )[1:]

    acc = 0
    for node in path:
        acc += grid[node.pos]
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
