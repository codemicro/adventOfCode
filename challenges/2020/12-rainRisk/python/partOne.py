from typing import Tuple

from common import *


bearings_num = {
    0: "n",
    90: "e",
    180: "s",
    270: "w",
}

bearings_ltr = {
    "n": 0,
    "e": 90,
    "s": 180,
    "w": 270,
}


def rotate_direction(current: str, direction: str, amount: int) -> str:

    assert direction in ["l", "r"], f"invalid rotate direction '{direction}'"

    current_bearing = bearings_ltr[current]

    if direction == "l":
        current_bearing -= amount
    elif direction == "r":
        current_bearing += amount

    if current_bearing >= 360:
        current_bearing -= 360
    elif current_bearing < 0:
        current_bearing += 360

    return bearings_num[current_bearing]


def translate_movement(
    current_direction: str, instruction: Instruction
) -> Tuple[str, int, int]:
    # Returns the new current direction and the lat/long delta

    lat_delta = 0
    long_delta = 0

    if instruction.action in ["l", "r"]:
        current_direction = rotate_direction(
            current_direction, instruction.action, instruction.magnitude
        )
    elif instruction.action == "f":
        lat_delta, long_delta = calculate_direction_deltas(
            current_direction, instruction.magnitude
        )
    elif instruction.action in ["n", "s", "e", "w"]:
        lat_delta, long_delta = calculate_direction_deltas(
            instruction.action, instruction.magnitude
        )
    else:
        raise AssertionError(f"invalid action '{instruction.action}'")

    return current_direction, lat_delta, long_delta


def partOne(instr: str) -> int:
    input_list = parse(instr)

    current_direction = "e"
    lat = 0  # north/south, pos/neg
    long = 0  # west/east, pos/neg

    for instruction in input_list:
        current_direction, lad, lod = translate_movement(current_direction, instruction)
        lat += lad
        long += lod

    # Calculate manhattan distance
    # If either value is negative, make it positive
    if lat < 0:
        lat = lat + -2 * lat
    if long < 0:
        long = long + -2 * long

    return lat + long
