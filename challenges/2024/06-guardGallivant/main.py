import sys
from gridutil import grid, coord
from typing import Optional
from tqdm import tqdm


def parse(instr: str) -> grid.Grid:
    return grid.parse(instr)


def find_start(g: grid.Grid) -> coord.Coordinate:
    for pos in g:
        if g[pos] == "^":
            return pos
    assert False, "no start point found"
    
    
def modplus(x: int) -> int:
    return (x + 1) % 4

    
dirs = [coord.Direction.Up, coord.Direction.Right, coord.Direction.Down, coord.Direction.Left]


class LoopEncounteredException(Exception):
    pass


def trace(g: grid.Grid, guard_pos: coord.Coordinate, guard_direction: int) -> set[tuple[coord.Coordinate, int]]:
    visited_sequence = set()
    
    while guard_pos in g:
        if (guard_pos, guard_direction) in visited_sequence:
            raise LoopEncounteredException
        
        visited_sequence.add((guard_pos, guard_direction))
        
        nc = coord.add(guard_pos, dirs[guard_direction % 4].delta())
        if nc in g and g[nc] == "#":
            guard_direction = modplus(guard_direction)
        else:
            guard_pos = nc

    return visited_sequence


def one(instr: str) -> int:
    g = parse(instr)
    return len(set(map(lambda x: x[0], trace(g, find_start(g), 0))))


def two(instr: str) -> int:
    g = parse(instr)
    
    start_pos = find_start(g)
    seq = trace(g, start_pos, 0)
    known_blocks = set()
    
    for (pos, _) in tqdm(seq, file=sys.stderr):
        assert pos in g, "pos off the rails"
        g[pos] = "#"
        try:
            trace(g, start_pos, 0)
        except LoopEncounteredException:
            known_blocks.add(pos)
        g[pos] = "."
    
    return len(known_blocks)


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