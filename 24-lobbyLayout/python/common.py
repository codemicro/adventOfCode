from typing import List, Tuple, Dict


def make_vector(loc: List[str], start: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    r, s = start

    for ins in loc:
        if ins == "nw":
            r -= 1
        elif ins == "ne":
            r -= 1
            s += 1
        elif ins == "w":
            s -= 1
        elif ins == "e":
            s += 1
        elif ins == "sw":
            r += 1
            s -= 1
        elif ins == "se":
            r += 1

    return r, s


def make_initial_state(tile_locations: List[List[str]]) -> Dict[Tuple[int, int], bool]:
    # True represents a black tile - false is white
    tiles = {}
    for loc in tile_locations:
        pos = make_vector(loc)
        tiles[pos] = not tiles.get(pos, False)
    return tiles


def count_black_tiles(tiles: Dict[Tuple[int, int], bool]) -> int:
    black_tiles = 0
    for key in tiles:
        if tiles[key]:
            black_tiles += 1
    return black_tiles


def parse(instr: str) -> List[str]:
    # e, se, sw, w, nw, and ne

    tiles = instr.strip().split("\n")
    o = []

    for tile_line in tiles:
        tl = []
        pointer = 0
        while pointer < len(tile_line):
            current = tile_line[pointer]
            if current in ["s", "n"]:
                tl.append(tile_line[pointer : pointer + 2])
                pointer += 2
            else:
                tl.append(current)
                pointer += 1
        o.append(tl)

    return o
