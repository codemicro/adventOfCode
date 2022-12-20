from __future__ import annotations
from pprint import pprint
from typing import *
from aocpy import BaseChallenge
from dataclasses import dataclass
import re
from math import inf
import itertools
import copy


@dataclass
class Node:
    name: str
    value: int
    edges: List[Node]

    def __init__(
        self, name: str, value: int = 0, edges: Optional[List[Tuple[Node, int]]] = None
    ):
        self.name = name
        self.value = value
        self.edges = [] if edges is None else edges


def shortest_path(nodes: Dict[str, Node], begin: str, end: str) -> List[str]:
    priorities: Dict[str, Tuple[Union[int, float], Optional[str]]] = {
        node: (inf, None) for node in nodes
    }
    visited: Dict[str, None] = {begin: None}

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
            if neighbour.name in visited:
                continue
            if priorities[neighbour.name][0] > length_to_current + 1:
                priorities[neighbour.name] = (length_to_current + 1, cursor)

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

    return route[:-1]


parse_re = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ((?:[A-Z]+,? ?)+)"
)


def parse(
    instr: str,
) -> Tuple[Dict[str, Node], List[str], Dict[Tuple[str, str], List[str]]]:
    sp = [parse_re.match(line).groups() for line in instr.strip().splitlines()]

    nodes: Dict[str, Node] = {}
    unjammed_nodes: List[str] = []
    for (valve_name, flow_rate_str, _) in sp:
        flow_rate = int(flow_rate_str)
        nodes[valve_name] = Node(valve_name, flow_rate)
        if flow_rate != 0:
            unjammed_nodes.append(valve_name)

    for (valve_name, _, further_nodes_str) in sp:
        n = nodes[valve_name]
        for connected_node_name in further_nodes_str.split(", "):
            n.edges.append(nodes[connected_node_name])

    # work out a matrix of the shortest paths between two nodes
    shortest_paths: Dict[Tuple[str, str], List[str]] = {}
    for start_node in nodes:

        if nodes[start_node].value == 0 and start_node != "AA":
            continue

        for end_node in nodes:
            if end_node == start_node or nodes[end_node].value == 0:
                continue

            path = shortest_path(nodes, start_node, end_node)
            pl = len(path) + 1
            shortest_paths[(start_node, end_node)] = pl
            shortest_paths[(end_node, start_node)] = pl

    return nodes, unjammed_nodes, shortest_paths


def permutations(
    current_node: str,
    nodes_remaining: List[str],
    shortest_paths: Dict[Tuple[str, str], List[str]],
    path: List[str],
    cost_remaining: int,
) -> Generator[List[str]]:
    for next_node in nodes_remaining:
        cost = shortest_paths[(current_node, next_node)]
        if cost < cost_remaining:
            nr = copy.copy(nodes_remaining)
            nr.remove(next_node)
            yield from permutations(
                next_node, nr, shortest_paths, path + [next_node], cost_remaining - cost
            )
    yield path


def calc_vented(
    nodes: Dict[str, Node],
    shortest_paths: Dict[Tuple[str, str], List[str]],
    visit_order: List[str],
    time_remaining: int,
) -> int:
    current = "AA"
    pressure = 0

    for node_name in visit_order:
        path_length = shortest_paths[(current, node_name)]
        time_remaining -= path_length + 1
        pressure += nodes[node_name].value * time_remaining
        current = node_name

    return pressure


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        nodes, unjammed_nodes, shortest_paths = parse(instr)

        max_pressure = 0
        for visit_order in permutations("AA", unjammed_nodes, shortest_paths, [], 30):
            pressure = calc_vented(nodes, shortest_paths, visit_order, 30)

            if pressure > max_pressure:
                max_pressure = pressure

        return max_pressure

    @staticmethod
    def two(instr: str) -> int:
        nodes, unjammed_nodes, shortest_paths = parse(instr)

        pressures = [
            (calc_vented(nodes, shortest_paths, visit_order, 26), visit_order)
            for visit_order in permutations(
                "AA", unjammed_nodes, shortest_paths, [], 26
            )
        ]

        max_pressure = 0
        for i, (pressure_a, order_a) in enumerate(
            sorted(pressures, reverse=True, key=lambda x: x[0])
        ):
            if pressure_a * 2 < max_pressure:
                break
            for (pressure_b, order_b) in pressures[i + 1 :]:
                if len(set(order_a).intersection(order_b)) == 0:
                    pressure = pressure_a + pressure_b
                    if pressure > max_pressure:
                        max_pressure = pressure

        return max_pressure
