import heapq
import queue
from typing import Any, Tuple, List, Dict, Optional
from aocpy import BaseChallenge
from dataclasses import dataclass

Point = Tuple[int, int]
Nodes = Dict[Point, int]


@dataclass
class Graph:
    nodes: Nodes
    edges: Dict[Point, List[Point]]


def get_adjacent_points(point: Point) -> List[Point]:
    x, y = point
    return [
        (x, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
    ]


def parse(instr: str, expand: bool) -> Graph:
    nodes = {}
    edges = {}

    lines = instr.strip().splitlines()
    num_lines = len(lines)
    line_len = len(lines[0])

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            number = int(char)
            nodes[(x, y)] = int(char)

            if expand:
                for my in range(5):
                    for mx in range(5):
                        nodes[x + (mx * line_len), y + (my * num_lines)] = ((number + my + mx - 1) % 9) + 1

    for node in nodes:
        edges[node] = edges.get(node, []) + [
            p for p in get_adjacent_points(node) if p in nodes
        ]

    return Graph(nodes, edges)


def get_shortest_path_len(graph: Graph) -> int:
    # ty https://old.reddit.com/r/adventofcode/comments/rgqzt5/2021_day_15_solutions/hooca55/

    start = (0, 0)
    end = (
        max(x for x, _ in graph.nodes),
        max(y for _, y in graph.nodes),
    )

    dist: Dict[Point, int] = {start: 0}
    pq: List[Tuple[int, Point]] = []

    for v in graph.nodes:
        if v != start:
            dist[v] = int(1e9)
        heapq.heappush(pq, (dist[v], v))

    while pq:
        _, u = heapq.heappop(pq)
        if u == end:
            return dist[end]
        for v in graph.edges[u]:
            if v not in graph.nodes:
                continue
            alt = dist[u] + graph.nodes[v]
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(pq, (alt, v))

    return dist[end]


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        g = parse(instr, False)
        return get_shortest_path_len(g)

    @staticmethod
    def two(instr: str) -> Any:
        g = parse(instr, True)
        return get_shortest_path_len(g)
