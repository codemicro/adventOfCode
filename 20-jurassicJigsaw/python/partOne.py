from common import *
from pprint import pprint


def partOne(instr: str) -> int:
    tiles = parse(instr)

    edges = {}

    # find dictionary of edges and the tiles that have them

    for tile in tiles:
        for edge in tile.edges:
            if edge not in edges:
                edges[edge] = set([tile.number])
            else:
                edges[edge].add(tile.number)

    to_del = []

    for edge in edges:
        rev = "".join(reversed(edge))
        if rev in edges and edge not in to_del:
            edges[edge].update(edges[rev])
            to_del.append(rev)

    for r in to_del:
        del edges[r]

    # count the number of shared edges each tile has

    shared_edge_count = {x.number:0 for x in tiles}
    for tile in tiles:
        for x in edges:
            tn = edges[x]
            if tile.number in tn and len(tn) > 1:
                shared_edge_count[tile.number] += 1

    # find the product of all tile numbers that have 2 matching edges

    pprint(shared_edge_count)

    c = 1
    for x in shared_edge_count:
        if shared_edge_count[x] == 2:
            c *= x

    return c
