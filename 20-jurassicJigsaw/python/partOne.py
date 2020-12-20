from common import *
from pprint import pprint


def partOne(instr: str) -> int:
    tiles = parse(instr)

    edges = {}

    for tile in tiles:
        for edge in tile.edges:
            if edge not in edges:
                edges[edge] = set([tile.number])
            else:
                edges[edge].add(tile.number)

    to_del = []

    for edge in edges:
        rev = "".join(reversed(edge))
        if rev in edges:
            edges[edge] = edges[edge].union(edges[rev])
            to_del.append(rev)

    for r in to_del:
        del edges[r]

    shared_edge_count = {x.number:0 for x in tiles}
    for tile in tiles:
        for x in edges:
            tn = edges[x]
            if tile.number in tn and len(tn) > 1:
                shared_edge_count[tile.number] += 1

    pprint(shared_edge_count)

    pprint(edges)

    return 0
