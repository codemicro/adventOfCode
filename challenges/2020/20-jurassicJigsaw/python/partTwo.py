from common import *


def partTwo(instr: str) -> int:
    tiles_list = parse(instr)
    edges, shared_edge_count = get_edge_information(tiles_list)

    # from here onwards, it's going to make more sense to use a dictionary that has tile numbers to the tile object
    tiles = {}
    for tile in tiles_list:
        tiles[tile.number] = tile

    used_tiles = []
    matrix = {}

    # get a single corner, set that as the start point
    for tile_id in shared_edge_count:
        if shared_edge_count[tile_id] == 2:
            matrix[(0, 0)] = tiles[tile_id].components

    print(matrix)

    return 0
