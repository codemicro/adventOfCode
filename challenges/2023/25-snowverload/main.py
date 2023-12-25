import sys
import networkx as nx
import random
from collections import defaultdict
from functools import reduce


def parse(instr: str) -> nx.Graph:
    g = nx.Graph()
    for line in instr.splitlines():
        node, next_nodes = line.split(": ")
        next_nodes = next_nodes.split(" ")
        for x in zip([node] * len(next_nodes), next_nodes):
            g.add_nodes_from(x)
            g.add_edge(*x, capacity=1)
    return g


def one(instr: str):
    g = parse(instr)
    nodes = list(g.nodes())

    cut = 0
    split_nodes = None

    while cut != 3:
        x = random.choices(nodes, k=2)
        if x[0] == x[1]:
            continue
        
        cut, nodes = nx.minimum_cut(g, *x, flow_func=nx.algorithms.flow.shortest_augmenting_path)
        split_nodes = nodes

    assert split_nodes is not None
    return reduce(lambda acc, x: acc * len(x), split_nodes, 1)


def two(_: str):
    return "Merry Christmas!"

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