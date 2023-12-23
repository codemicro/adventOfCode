import sys
import gridutil.grid as gu
import gridutil.coord as cu
from collections import namedtuple
from collections.abc import Generator


def parse(instr: str) -> gu.Grid:
    return gu.parse(instr)


def get_terminal_points(forest: gu.Grid) -> tuple[cu.Coordinate, cu.Coordinate]:
    start_pos = None
    end_pos = None
    max_y = gu.get_max_y(forest)
    for x in range(gu.get_max_x(forest) + 1):
        if forest[(x, 0)] == "." and start_pos is None:
            start_pos = cu.Coordinate(x, 0)
        if forest[(x, max_y)] == "." and end_pos is None:
            end_pos = cu.Coordinate(x, max_y)

    if start_pos is None:
        raise ValueError("No open cell found on the first row of the forest")

    if end_pos is None:
        raise ValueError("No open cell found on the last row of the forest")

    return start_pos, end_pos


def trace_path(
    forest: gu.Grid,
    start_pos: cu.Coordinate,
    end_pos: cu.Coordinate,
    history: set[cu.Coordinate] | None = None,
    n: int = 0,
    disallowed_moves: dict[str, cu.Direction] | None = None,
) -> int:
    if history is None:
        history = set()

    if disallowed_moves is None:
        disallowed_moves = {}

    cursor = start_pos
    while cursor != end_pos:
        history.add(cursor)
        allowable = []
        for direction in cu.Direction:
            target_pos = cu.add(cursor, direction.delta())

            if target_pos not in forest or target_pos in history:
                continue

            val = forest[target_pos]

            if val == "#" or direction == disallowed_moves.get(val):
                continue

            allowable.append(target_pos)

        n += 1

        match len(allowable):
            case 0:
                return -1
            case 1:
                cursor = allowable[0]
            case _:
                highest = max(
                    trace_path(
                        forest,
                        x,
                        end_pos,
                        history=history.copy(),
                        n=n,
                        disallowed_moves=disallowed_moves,
                    )
                    for x in allowable
                )
                return highest

    return n


def one(instr: str):
    forest = parse(instr)
    start_pos, end_pos = get_terminal_points(forest)
    return trace_path(
        forest,
        start_pos,
        end_pos,
        disallowed_moves={
            "^": cu.Direction.Down,
            "v": cu.Direction.Up,
            ">": cu.Direction.Left,
            "<": cu.Direction.Right,
        },
    )


DistanceTo: tuple[cu.Coordinate, int] = namedtuple(
    "DistanceTo", ["coordinate", "distance"]
)


def neighbours(
    forest: gu.Grid, pos: cu.Coordinate
) -> Generator[cu.Coordinate, None, None]:
    for direction in cu.Direction:
        target = cu.add(pos, direction.delta())
        if target not in forest or forest[target] == "#":
            continue
        yield target


def build_graph(
    forest: gu.Grid, start_pos: cu.Coordinate
) -> dict[cu.Coordinate, list[DistanceTo]]:
    junctions = [start_pos]
    graph = {}

    while junctions:
        st = junctions.pop(0)

        possible_next = list(neighbours(forest, st))
        routes = []

        for start_point in possible_next:
            n = 0
            cursor = start_point
            history = set([start_point, st])
            get_next_steps = lambda: list(
                filter(
                    lambda x: x not in history,
                    neighbours(forest, cursor),
                )
            )
            next_steps = get_next_steps()

            while len(next_steps) == 1:
                n += 1
                cursor = next_steps[0]
                history.add(cursor)
                next_steps = get_next_steps()

            routes.append(DistanceTo(cursor, n + 1))
            if cursor not in graph:
                junctions.append(cursor)

        graph[st] = routes

    return graph


def display_graph(graph: dict[cu.Coordinate, list[DistanceTo]]):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()

    for node in graph:
        for (end, length) in graph[node]:
            G.add_edge(node, end, weight=length)

    nx.draw(G, with_labels=True, font_weight="bold")
    plt.show()


def trace_graph_path(
    graph: dict[cu.Coordinate, list[DistanceTo]],
    start_pos: cu.Coordinate,
    end_pos: cu.Coordinate,
    history: set[cu.Coordinate] | None = None,
    n: int = 0,
) -> int:
    if history is None:
        history = set()

    if start_pos == end_pos:
        return n

    history.add(start_pos)
    adjacent = list(filter(lambda x: x.coordinate not in history, graph[start_pos]))

    if len(adjacent) == 0:
        return -1

    for edge in adjacent:
        if edge.coordinate == end_pos:
            return edge.distance + n

    return max(
        trace_graph_path(
            graph, p.coordinate, end_pos, history=history.copy(), n=n + p.distance
        )
        for p in adjacent
    )


def two(instr: str):
    forest = parse(instr)
    start_pos, end_pos = get_terminal_points(forest)
    graph = build_graph(forest, start_pos)
    # display_graph(graph)
    return trace_graph_path(graph, start_pos, end_pos)


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
