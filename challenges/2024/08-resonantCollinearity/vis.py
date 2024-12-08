import sys
from gridutil import grid, coord
from collections import defaultdict
import itertools
from fractions import Fraction
import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from colorsys import hsv_to_rgb


def parse(instr: str) -> tuple[dict[str, list[coord.Coordinate]], tuple[int, int]]:
    g = grid.parse(instr)
    antenna_by_type = defaultdict(list)
    for key in g:
        if g[key] == ".":
            continue
        antenna_by_type[g[key]].append(key)
    return antenna_by_type, (grid.get_max_x(g), grid.get_max_y(g))


lowest_colour = (255, 245, 237)
highest_colour = (255, 159, 45)
highlight_colour = (255, 47, 47)
shadow_colour = (226, 218, 211)
colour_diffs = tuple(map(lambda x: x[1] - x[0], zip(highest_colour, lowest_colour)))


def get_colour_for(n):
    return tuple(
        map(
            int,
            map(
                lambda x: x[0] - x[1],
                zip(lowest_colour, map(lambda x: x * n, colour_diffs)),
            ),
        )
    )


scale_factor = 8


def get_highlight_for(n):
    return tuple(map(lambda x: int(x * 255), hsv_to_rgb(n, 0.82, 1)))


def generate_frame(i, base_img, highlight_locs, hc, sequence) -> int:
    for n in range(len(sequence)):
        s = sequence[: n + 1]
        img = base_img.copy()

        sl = len(s) + 1
        for j, p in enumerate(s):
            img.putpixel(p, get_colour_for((j + 1) / sl))

        for h in highlight_locs:
            img.putpixel(h, hc)

        maxx, maxy = img.size
        img = img.resize(
            (maxx * scale_factor, maxy * scale_factor), resample=Image.NEAREST
        )
        img.save(f"frames/{str(i).zfill(5)}.png")
        i += 1
    return i


def update_base(base_img, add):
    for v in add:
        base_img.putpixel(v, shadow_colour)


if __name__ == "__main__":
    inp = sys.stdin.read().strip()
    (antenna_by_type, (max_x, max_y)) = parse(inp)

    ns = list(sorted(antenna_by_type.keys()))
    nns = len(ns)

    try:
        os.makedirs("frames")
    except FileExistsError:
        pass

    base_img = Image.new("RGB", (max_x + 1, max_y + 1), color=lowest_colour)

    i = 0
    for antenna_type in tqdm(antenna_by_type):
        for (a, b) in itertools.permutations(antenna_by_type[antenna_type], 2):
            if (
                a.x > b.x
            ):  # filter out (most) duplicate pairs eg ((1, 2), (2, 1)) will only be calculated as ((2, 1), (1, 2)) will be filtered. This also prevents diff.x from being negative (useful for the mod operation)
                continue

            this_iter = []

            diff = coord.sub(b, a)

            m = Fraction(
                diff.y, diff.x
            )  # equiv of diff.y / diff.x but without the 26.9999999999996 issue
            c = a.y - (m * a.x)

            x_cursor = a.x % diff.x
            y_cursor = int((x_cursor * m) + c)
            while x_cursor <= max_x:
                if 0 <= y_cursor <= max_y:
                    this_iter.append((x_cursor, y_cursor))
                x_cursor += diff.x
                y_cursor += diff.y

            i = generate_frame(
                i,
                base_img,
                (a, b),
                get_highlight_for(ns.index(antenna_type) / nns),
                this_iter,
            )
            update_base(base_img, this_iter)
