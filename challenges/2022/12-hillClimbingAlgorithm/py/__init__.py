from __future__ import annotations
from dataclasses import dataclass
from math import inf, sqrt
from typing import *
from aocpy import BaseChallenge, Vector


CARDINAL_DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))


@dataclass
class Node:
    pos: Vector
    value: int
    edges: List[Node]

    def __init__(
        self,
        pos: Vector,
        value: int = 0,
        edges: Optional[List[Tuple[Node, int]]] = None,
    ):
        self.pos = pos
        self.value = value
        self.edges = [] if edges is None else edges


def parse(instr: str) -> Tuple[Dict[Vector, Node], Vector, Vector]:

    start: Vector
    end: Vector

    nodes: Dict[Vector, Node] = {}
    for y, line in enumerate(instr.strip().splitlines()):
        for x, char in enumerate(line):

            conv_char = char
            if char == "S":
                conv_char = "a"
            elif char == "E":
                conv_char = "z"

            v = Vector(x, y)

            height = ord(conv_char) - ord("a")
            n = Node(v, height)
            nodes[v] = n

            if char == "S":
                start = n.pos
            elif char == "E":
                end = n.pos

    for coord in nodes:
        n = nodes[coord]

        for modifier in CARDINAL_DIRECTIONS:
            check = coord + modifier
            adjacent_node = nodes.get(check)

            if adjacent_node is not None:
                if adjacent_node.value - n.value < 2:
                    n.edges.append(adjacent_node)

    return nodes, start, end


def shortest_path(nodes: Dict[Vector, Node], begin: Vector, end: Vector) -> int:
    priorities: Dict[Vector, Tuple[Union[int, float], Optional[Vector]]] = {
        node: (inf, None) for node in nodes
    }
    visited: Dict[Vector, None] = {begin: None}

    cursor = begin
    while True:
        if cursor == end:
            break

        n = nodes[cursor]
        visited[cursor] = None

        length_to_current = priorities[cursor][0]
        if length_to_current == inf:
            length_to_current = 0

        # every neighbour that's not been visited already
        for neighbour in n.edges:
            if neighbour.pos in visited:
                continue
            if priorities[neighbour.pos][0] > length_to_current + 1:
                priorities[neighbour.pos] = (length_to_current + 1, cursor)

        # work out next item
        min_priority = (inf, None)
        for node_name in priorities:
            if node_name not in visited and priorities[node_name][0] < min_priority[0]:
                min_priority = (priorities[node_name][0], node_name)

        cursor = min_priority[1]

    route: List[str] = []
    while priorities[cursor][1] is not None:
        route.insert(0, cursor)
        cursor = priorities[cursor][1]

    return len(route)


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        nodes, start, end = parse(instr)
        return shortest_path(nodes, start, end)

    @staticmethod
    def two(instr: str) -> int:
        nodes, _, end = parse(instr)

        # possible starting positions are ones with value=0 bordering one with value=1

        starting_positions: List[Vector] = []
        for coord in nodes:
            node = nodes[coord]
            if node.value != 0:
                continue

            for adj_node in node.edges:
                if adj_node.value == 1:
                    starting_positions.append(coord)
                    break

        shortest = inf
        for coord in starting_positions:
            x = shortest_path(nodes, coord, end)
            if x < shortest:
                shortest = x

        return shortest
