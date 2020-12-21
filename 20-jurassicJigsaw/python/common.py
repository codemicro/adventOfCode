from typing import List, Set, Dict, Tuple
import re


def get_tile_edges(tile: List[List[str]]) -> List[str]:
    # returns edges in order: top, bottom, left, right
    edges = []
    edges.append("".join(tile[0]))
    edges.append("".join(tile[-1]))
    edges.append("".join([tile[x][0] for x in range(len(tile))]))
    edges.append("".join([tile[x][-1] for x in range(len(tile))]))
    return edges


class Tile:
    components: List[List[str]]
    edges: List[str]
    number: int

    def __init__(self, instr: str) -> None:
        split_input = instr.strip().split("\n")
        self.number = int(re.search(r"Tile (\d+)", split_input[0]).group(1))
        self.components = [list(x) for x in split_input[1:]]

        self.edges = get_tile_edges(self.components)


def parse(instr: str) -> List[Tile]:
    return [Tile(x) for x in instr.strip().split("\n\n")]


def get_edge_information(
    tiles: List[Tile],
) -> Tuple[Dict[str, Set[int]], Dict[int, int]]:
    edges = {}
    shared_edge_count = {x.number: 0 for x in tiles}

    # find dictionary of edges and the tiles that have them
    for tile in tiles:
        for edge in tile.edges:
            if edge not in edges:
                edges[edge] = set([tile.number])
            else:
                edges[edge].add(tile.number)

    # combine edges that are reversed versions of each other
    to_del = []
    for edge in edges:
        rev = "".join(reversed(edge))
        if rev in edges and edge not in to_del:
            edges[edge].update(edges[rev])
            to_del.append(rev)
    for r in to_del:
        del edges[r]

    # count the number of shared edges each tile has
    for tile in tiles:
        for x in edges:
            tn = edges[x]
            if tile.number in tn and len(tn) > 1:
                shared_edge_count[tile.number] += 1

    return edges, shared_edge_count
