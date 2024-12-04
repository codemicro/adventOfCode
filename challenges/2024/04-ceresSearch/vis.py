import sys
import gridutil.grid as grid
import gridutil.coord as coord
from collections import defaultdict
import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm


def parse(instr: str) -> grid.Grid:
    return grid.parse(instr.upper())

def one(instr: str):
    wordsearch = parse(instr)

    seq_starts = list(
        map(lambda x: x[0], filter(lambda x: x[1] == "X", wordsearch.items()))
    )
    detected_sequences = set()

    for start_pos in seq_starts:
        for xdir in [-1, 0, 1]:
            for ydir in [-1, 0, 1]:

                if xdir == 0 and ydir == 0:
                    continue

                delta = coord.Coordinate(xdir, ydir)

                ok = True
                b = []
                for i, v in enumerate("XMAS"):
                    if not ok:
                        break

                    x = coord.add(start_pos, coord.mult(delta, i))
                    g = wordsearch.get(x, "-")
                    ok = g == v
                    b.append(x)

                if ok:
                    detected_sequences.add(tuple(b))

    return detected_sequences


def check_cross_adjacents(s: str) -> bool:
    return s == "SM" or s == "MS"


def two(instr: str):
    wordsearch = parse(instr)

    seq_starts = list(
        map(lambda x: x[0], filter(lambda x: x[1] == "A", wordsearch.items()))
    )
    detected_sequences = set()

    for start_pos in seq_starts:

        a = wordsearch.get(coord.add(start_pos, (-1, -1)), "") + wordsearch.get(
            coord.add(start_pos, (1, 1)), ""
        )
        b = wordsearch.get(coord.add(start_pos, (-1, 1)), "") + wordsearch.get(
            coord.add(start_pos, (1, -1)), ""
        )

        if check_cross_adjacents(a) and check_cross_adjacents(b):
            detected_sequences.add(start_pos)

    return detected_sequences


lowest_colour = (255, 245, 237)
highest_colour = (255, 159, 45)
colour_diffs = tuple(map(lambda x: x[1] - x[0], zip(highest_colour, lowest_colour)))


def get_colour_for(n):
    return tuple(
        map(int, map(lambda x: x[0] - x[1], zip(lowest_colour, map(lambda x: x * n, colour_diffs))))
    )


scale_factor = 4

def generate_frame(path: str, wordsearch: grid.Grid, counts: dict[coord.Coordinate, int]):
    max_val = max(counts.values())
    
    maxx, maxy = grid.get_max_x(wordsearch), grid.get_max_y(wordsearch)
            
    img = Image.new("RGB", (maxx+1, maxy+1))
    
    for x in range(maxx+1):
        for y in range(maxy+1):
            img.putpixel((x, y), get_colour_for(counts[(x, y)]/max_val))

    img = img.resize((maxx * scale_factor, maxy * scale_factor), resample=Image.NEAREST)
    img.save(path)


def main():
    inp = sys.stdin.read().strip()
    wordsearch = parse(inp)
        
    j = defaultdict(lambda: 0)
    for state in one(inp):
        for s in state:
            j[s] = j[s] + 1
    generate_frame("heatmap-1.png", wordsearch, j)
    
    j = defaultdict(lambda: 0)
    for state in two(inp):
        for dir in [(0, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
            s = coord.add(state, dir)
            j[s] = j[s] + 1
    generate_frame("heatmap-2.png", wordsearch, j)
    

if __name__ == "__main__":
    main()