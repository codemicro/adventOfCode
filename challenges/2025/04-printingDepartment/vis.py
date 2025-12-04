import main
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import os
import sys
from tqdm import tqdm
from collections import defaultdict
from copy import copy


background_colour = (0, 0, 0)
foreground_colour = (255, 255, 255)
selected_colour = (0xB8, 0xBB, 0x26)
scan_colour = (0x45, 0x85, 0x88)

font_size = 3
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/jetbrainsmono/JetBrainsMono-Regular.ttf", font_size
)

frame_dir = Path("frames")
os.makedirs(frame_dir, exist_ok=True)


frame_counter = 0


def save_frame(img):
    global frame_counter
    frame_counter += 1
    img.save(frame_dir / f"{str(frame_counter).zfill(5)}.png")


def make_image(x, y):
    return Image.new("RGB", (x, y), color=background_colour)


def draw_grid(img, grid):
    draw = ImageDraw.Draw(img)
    for pos in tqdm(grid, position=1, leave=False):
        if grid[pos] == "@":
            draw.text((pos.x * font_size, pos.y * font_size), grid[pos], font=font)


def draw_scan_frames(img, szx, szy, to_change):
    idraw = ImageDraw.Draw(img)
    sets = defaultdict(list)
    for q in to_change:
        sets[q.y].append(q)
    for y in tqdm(range(szy + 1), position=1, leave=False):
        eimg = img.copy()
        draw = ImageDraw.Draw(eimg)
        draw.rectangle(
            ((0, y * font_size), (szx * font_size, (y + 1) * font_size)),
            fill=scan_colour,
        )
        save_frame(eimg)
        for (x, yy) in sets[y]:
            idraw.rectangle(
                (
                    (x * font_size, yy * font_size),
                    ((x + 1) * font_size, (yy + 1) * font_size),
                ),
                fill=selected_colour,
            )


if __name__ == "__main__":
    grid = main.parse(sys.stdin.read().strip())
    grid_size_x = max(filter(lambda x: x.x, grid.keys())).x
    grid_size_y = max(filter(lambda x: x.y, grid.keys())).y

    img_size_x = grid_size_x * font_size
    img_size_y = grid_size_y * font_size

    res = []
    change = 1
    while change != 0:
        to_remove = main.collect_movable(grid)
        change = len(to_remove)
        res.append((copy(grid), to_remove))
        for pos in to_remove:
            grid[pos] = "."

    for (grid, to_remove) in tqdm(res, position=0):
        base_img = make_image(img_size_x, img_size_y)
        draw_grid(base_img, grid)
        save_frame(base_img)
        draw_scan_frames(base_img, grid_size_x, grid_size_y, to_remove)
