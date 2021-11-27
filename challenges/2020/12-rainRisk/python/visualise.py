import common
import partOne
import partTwo
import os
from PIL import Image
import ffmpeg
import shutil
from tqdm import tqdm
from skimage.draw import line as bresline

from typing import Tuple, List


anim_counter = 0
frame_counter = 0


background_colour = "#000"
ship_colour = (190, 52, 58)
waypoint_colour = (52, 190, 58)
path_colour = (50, 49, 49)


resize_factor = 4


def make_frame(
    location_history: List[Tuple[int, int]],
    waypoint_history: List[Tuple[int, int]] = None,
    target_height: int = 160,
):
    global frame_counter  # muahahaha

    frame_size_lat = max([lc[0] for lc in location_history])
    frame_size_long = max([lc[1] for lc in location_history])

    latmod = min([lc[0] for lc in location_history])
    longmod = min([lc[1] for lc in location_history])

    print(frame_size_lat, frame_size_long, latmod, longmod)

    if latmod < 0:
        latmod = latmod + -2 * latmod
    if longmod < 0:
        longmod = longmod + -2 * longmod

    for i, lc in enumerate(location_history):
        location_history[i] = (lc[0] + latmod, lc[1] + longmod)

    if waypoint_history is not None:
        for i, wc in enumerate(waypoint_history):
            waypoint_history[i] = (wc[0] + latmod, wc[1] + longmod)

    frame_size_lat = max([lc[0] for lc in location_history])
    frame_size_long = max([lc[1] for lc in location_history])

    shrink_factor = int(frame_size_long / target_height)

    for i, lc in enumerate(location_history):
        location_history[i] = (
            int((lc[0] + latmod) / shrink_factor),
            int((lc[1] + longmod) / shrink_factor),
        )

    if waypoint_history is not None:
        for i, wc in enumerate(waypoint_history):
            waypoint_history[i] = (
                int((wc[0] + latmod) / shrink_factor),
                int((wc[1] + longmod) / shrink_factor),
            )

    frame_size_lat = max([lc[0] for lc in location_history])
    frame_size_long = max([lc[1] for lc in location_history])

    frame_size = (frame_size_lat + 1, frame_size_long + 1)

    print(frame_size)

    img = Image.new("RGB", frame_size, color=background_colour)

    last = None

    for i in tqdm(range(len(location_history))):
        lc = location_history[i]

        if last is not None:

            ln = bresline(last[0], last[1], lc[0], lc[1])
            xs = ln[0]
            ys = ln[1]

            for pxl in zip(xs, ys):
                img.putpixel(pxl, path_colour)

        else:
            img.putpixel(lc, path_colour)

        last = lc

        temp = img.copy()

        if waypoint_history is not None:
            temp.putpixel(waypoint_history[i], waypoint_colour)

        temp.putpixel(lc, ship_colour)

        new_width = int((temp.width * resize_factor) / 2) * 2
        new_height = int((temp.height * resize_factor) / 2) * 2
        temp = temp.resize((new_width, new_height), resample=Image.NEAREST)
        temp.save(
            os.path.join("output", f"{anim_counter}_{str(frame_counter).zfill(4)}.png")
        )
        frame_counter += 1


def partOneMod(instr: str) -> int:
    input_list = common.parse(instr)

    current_direction = "e"
    lat = 0  # north/south, pos/neg
    long = 0  # west/east, pos/neg

    location_history = []

    for instruction in input_list:
        current_direction, lad, lod = partOne.translate_movement(
            current_direction, instruction
        )
        lat += lad
        long += lod
        location_history.append((lat, long))

    return location_history


def partTwoMod(instr: str) -> int:
    input_list = common.parse(instr)

    waypoint_delta = (1, 10)
    lat = 0  # north/south, pos/neg
    long = 0  # west/east, pos/neg

    location_history = []
    waypoint_history = []

    for instruction in input_list:
        waypoint_delta, lad, lod = partTwo.translate_movement(
            waypoint_delta, instruction
        )
        lat += lad
        long += lod
        location_history.append((lat, long))
        waypoint_history.append((lat + waypoint_delta[0], long + waypoint_delta[1]))

    return location_history, waypoint_history


def visualise(instr: str):

    global anim_counter
    global frame_counter

    if os.path.exists("output"):
        shutil.rmtree("output")
    os.mkdir("output")

    one_location_history = partOneMod(instr)
    two_location_history, two_waypoint_history = partTwoMod(instr)

    # run one
    make_frame(one_location_history)
    anim_counter += 1
    frame_counter = 0
    make_frame(two_location_history, waypoint_history=two_waypoint_history)
    # run two

    for i in range(anim_counter + 1):
        if os.path.exists(f"{i}.gif"):
            os.unlink(f"{i}.gif")
        (
            ffmpeg.input(
                os.path.join("output", f"{i}_%04d.png"), framerate=30, start_number=0
            )
            .output(f"{i}.gif")
            .run()
        )

    shutil.rmtree("output")
