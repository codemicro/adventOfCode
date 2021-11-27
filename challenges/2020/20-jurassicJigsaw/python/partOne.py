from common import *
from pprint import pprint


def partOne(instr: str) -> int:
    tiles = parse(instr)

    _, shared_edge_count = get_edge_information(tiles)

    # find the product of all tile numbers that have 2 matching edges

    c = 1
    for x in shared_edge_count:
        if shared_edge_count[x] == 2:
            c *= x

    return c
