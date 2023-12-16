#!/usr/bin/env python3

import main
import os
from pathlib import Path
from PIL import Image
import sys
from typing import Optional


DIGIT_FONT = [
    [[(True if char == "x" else False) for char in line] for line in block.splitlines()]
    for block in open("digits.txt").read().split("\n\n")
]

background_colour = (0, 0, 0)  # black
stationary_colour = (190, 52, 58)  # red
falling_colour = (50, 49, 49)  # grey
scan_colour = (52, 190, 58)  # green
alt_scan_colour = (24, 77, 191)  # blue
letter_colour = (255, 255, 255)  # white

frame_dir = Path("frames")
os.mkdir(frame_dir)

counter = 0
frame_number = 0
scale_factor = 4


def draw_frame(
    platform: tuple[str],
    highlight_y: Optional[int] = None,
    allow_skip: bool = True,
    number: Optional[int] = None,
):
    global frame_number, counter

    counter += 1
    if not highlight_y and allow_skip:
        if counter % 21 != 0:
            return

    y = len(platform)
    x = len(platform[0])

    img = Image.new("RGB", (x, y), color=background_colour)

    for y, line in enumerate(platform):
        for x, char in enumerate(line):
            c = background_colour

            if char == "#":
                c = stationary_colour
            if char == "O":
                c = falling_colour
            if highlight_y is not None and y == highlight_y:
                if char == "O":
                    c = alt_scan_colour
                else:
                    c = scan_colour

            img.putpixel((x, y), c)

    if number is not None:
        pos_x = 5
        pos_y = 5

        for digit in str(number):
            digit = int(digit)
            for yd, line in enumerate(DIGIT_FONT[digit]):
                for xd, putpix in enumerate(line):
                    if putpix:
                        img.putpixel((pos_x + xd, pos_y + yd), letter_colour)
            pos_x += 7  # 5 pixel wide font + 2 pixel gap

    img = img.resize((x * scale_factor, y * scale_factor), resample=Image.NEAREST)
    img.save(frame_dir / f"{str(frame_number).zfill(8)}.png")
    frame_number += 1


def modtilt(
    platform: tuple[str], direction: main.TiltDirection, allow_skip=True, partial=True
) -> tuple[str]:
    needs_flip = (
        direction == main.TiltDirection.North or direction == main.TiltDirection.South
    )

    if direction == main.TiltDirection.North or direction == main.TiltDirection.South:
        platform = main.flip_platform(platform)

    if direction == main.TiltDirection.North or direction == main.TiltDirection.West:
        transformation = lambda x: x.replace(".O", "O.")
    else:
        transformation = lambda x: x.replace("O.", ".O")

    res = list(platform)

    changes = True

    while changes:
        changes = False
        for i in range(len(res)):
            after = transformation(res[i])
            if res[i] != after:
                changes = True
            res[i] = after
        if (partial and not changes) or not partial:
            draw_frame(
                res if not needs_flip else main.flip_platform(res),
                allow_skip=allow_skip,
            )

    if direction == main.TiltDirection.North or direction == main.TiltDirection.South:
        res = main.flip_platform(res)

    return tuple(res)


platform = main.parse(sys.stdin.read().strip())

draw_frame(platform)
platform = modtilt(platform, main.TiltDirection.North, allow_skip=False, partial=False)

acc = 0
for y, line in enumerate(platform):
    for x, char in enumerate(line):
        if char != "O":
            continue
        acc += len(platform) - y
    draw_frame(platform, highlight_y=y, number=acc)

for i in range(20):
    draw_frame(platform, number=acc, allow_skip=False)

platform = modtilt(platform, main.TiltDirection.West)
platform = modtilt(platform, main.TiltDirection.North)
platform = modtilt(platform, main.TiltDirection.East)

ITERS = 1_000_000_000 - 1

i = 0
known = {}
jumped = False
while i < ITERS:
    print(f"{i}/{ITERS}", end="\r")
    for direction in [
        main.TiltDirection.North,
        main.TiltDirection.West,
        main.TiltDirection.South,
        main.TiltDirection.East,
    ]:
        platform = modtilt(platform, direction)

    if not jumped:
        if platform in known:
            last_occurrence = known[platform]
            period = i - last_occurrence
            i += ((ITERS - i) // period) * period
            jumped = True
        else:
            known[platform] = i
    i += 1

acc = 0
for y, line in enumerate(platform):
    for x, char in enumerate(line):
        if char != "O":
            continue
        acc += len(platform) - y
    draw_frame(platform, highlight_y=y, number=acc)

for i in range(20):
    draw_frame(platform, number=acc, allow_skip=False)
