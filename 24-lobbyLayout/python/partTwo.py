from common import *


offsets = (
    (-1, 0),
    (-1, +1),
    (0, -1),
    (0, +1),
    (+1, -1),
    (+1, 0),
)


def count_neighbours(tiles: Dict[Tuple[int, int], bool], pos: Tuple[int, int]) -> int:
    count = 0
    r, s = pos
    for ro, so in offsets:
        if tiles.get((r + ro, s + so), False):
            count += 1
    return count


def iterate(tiles: Dict[Tuple[int, int], bool]) -> None:
    changes = {}

    min_r, _ = min(tiles, key=lambda x: x[0])
    max_r, _ = max(tiles, key=lambda x: x[0])
    _, min_s = min(tiles, key=lambda x: x[1])
    _, max_s = max(tiles, key=lambda x: x[1])

    for r in range(min_r - 2, max_r + 2):
        for s in range(min_s - 2, max_s + 2):
            neighbours = count_neighbours(tiles, (r, s))
            current_state = tiles.get((r, s), False)  # true is black, false is white

            # black tile with zero or more than 2 black tiles adjacent is flipped to white.
            if current_state and (neighbours == 0 or neighbours > 2):
                changes[(r, s)] = False
            # white tile with exactly 2 black tiles adjacent is flipped to black.
            elif not current_state and neighbours == 2:
                changes[(r, s)] = True

    # apply changes to master dictionary
    for pos in changes:
        ns = changes[pos]
        if changes[pos]:
            tiles[pos] = ns
        else:
            del tiles[pos]

    return


def partTwo(instr: str) -> int:
    tiles_locations = parse(instr)
    tiles = make_initial_state(tiles_locations)

    for _ in range(100):
        iterate(tiles)

    return count_black_tiles(tiles)
