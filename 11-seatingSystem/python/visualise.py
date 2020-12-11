import common
import partOne
import partTwo
import os
from PIL import Image
import ffmpeg
import shutil

from typing import Callable, List

frame_counter = 1
anim_counter = 0
skipped_last = True

background_colour = "#646464"
occupied_colour = (230, 0, 0)
empty_colour = (100, 220, 100)

resize_factor = 3


def make_frame(hall: List[List[str]]):
    global frame_counter, skipped_last  # muahahaha

    if not skipped_last:
        skipped_last = True
        return
    else:
        skipped_last = False

    hall_size = (len(hall[0]), len(hall))

    img = Image.new("RGB", hall_size, color=background_colour)

    for x in range(hall_size[0]):
        for y in range(hall_size[1]):

            jts = hall[y][x]

            if jts == common.no_seat:
                continue

            colour = None
            if jts == common.open_seat:
                colour = empty_colour
            elif jts == common.filled_seat:
                colour = occupied_colour
            else:
                continue

            img.putpixel((x, y), colour)

    new_width = int((img.width * resize_factor) / 2) * 2
    new_height = int((img.height * resize_factor) / 2) * 2

    img = img.resize((new_width, new_height), resample=Image.NEAREST)

    img.save(
        os.path.join("output", f"{anim_counter}_{str(frame_counter).zfill(4)}.png")
    )
    frame_counter += 1


def run(
    current_state: List[List[str]],
    neighbour_counter: Callable,
    get_new_state: Callable,
    hook: Callable,
):
    last_state = None

    while current_state != last_state:
        hook(current_state)
        last_state = current_state
        current_state = common.iterate(current_state, neighbour_counter, get_new_state)


def visualise(instr: str):

    global anim_counter
    global frame_counter

    if not os.path.exists("output"):
        os.mkdir("output")

    run(
        common.parse(instr), partOne.count_neighbours, partOne.get_new_state, make_frame
    )
    anim_counter += 1
    frame_counter = 0
    skipped_last = True
    run(
        common.parse(instr), partTwo.count_neighbours, partTwo.get_new_state, make_frame
    )

    for i in range(anim_counter + 1):
        if os.path.exists(f"{i}.gif"):
            os.unlink(f"{i}.gif")
        (
            ffmpeg.input(
                os.path.join("output", f"{i}_%04d.png"), framerate=10, start_number=0
            )
            .output(f"{i}.gif")
            .run()
        )

    shutil.rmtree("output")
