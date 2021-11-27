from common import *


def partOne(instr: str) -> int:
    tiles_locations = parse(instr)
    tiles = make_initial_state(tiles_locations)
    return count_black_tiles(tiles)
