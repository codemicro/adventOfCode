from typing import Tuple

from common import *


def make_positive(n: int) -> int:
    return n if n >= 0 else n + -2 * n


def make_negative(n: int) -> int:
    return n if n < 0 else n + -2 * n


def rotate_waypoint(
    current: Tuple[int, int], direction: str, amount: int
) -> Tuple[int, int]:

    assert direction in ["l", "r"], f"invalid rotate direction '{direction}'"

    lat_delta, long_delta = current

    times = int(amount / 90)  # number of times to rotate the waypoint by

    # Determine the current quadrant
    quadrant = None
    if lat_delta >= 0 and long_delta >= 0:
        quadrant = 1
    elif lat_delta < 0 and long_delta >= 0:
        quadrant = 2
    elif lat_delta < 0 and long_delta < 0:
        quadrant = 3
    elif lat_delta >= 0 and long_delta < 0:
        quadrant = 4

    assert quadrant is not None, f"unable to determine quadrant for {current}"

    # Determine the new quadrant
    new_quadrant = quadrant
    if direction == "r":
        new_quadrant += times
    elif direction == "l":
        new_quadrant -= times

    # Loop quadrant around if it went outside of 1-4
    if new_quadrant > 4:
        new_quadrant -= 4
    elif new_quadrant < 1:
        new_quadrant += 4

    # Swap values if the new quadrant is not the opposite one
    quadrant_diff = quadrant - new_quadrant
    if quadrant_diff % 2 != 0:
        t = lat_delta
        lat_delta = long_delta
        long_delta = t

    # Transform deltas into their new quadrant
    if new_quadrant == 1:
        lat_delta = make_positive(lat_delta)
        long_delta = make_positive(long_delta)
    elif new_quadrant == 2:
        lat_delta = make_negative(lat_delta)
        long_delta = make_positive(long_delta)
    elif new_quadrant == 3:
        lat_delta = make_negative(lat_delta)
        long_delta = make_negative(long_delta)
    elif new_quadrant == 4:
        lat_delta = make_positive(lat_delta)
        long_delta = make_negative(long_delta)

    return lat_delta, long_delta


def move_to_waypoint(waypoint_delta: Tuple[int, int], times: int) -> Tuple[int, int]:
    lat_delta, long_delta = waypoint_delta
    return lat_delta * times, long_delta * times


def translate_movement(
    waypoint_delta: Tuple[int, int], instruction: Instruction
) -> Tuple[Tuple[int, int], int, int]:
    # Returns the new current direction and the lat/long delta

    lat_delta = 0
    long_delta = 0

    if instruction.action in ["l", "r"]:
        waypoint_delta = rotate_waypoint(
            waypoint_delta, instruction.action, instruction.magnitude
        )
    elif instruction.action == "f":
        lat_delta, long_delta = move_to_waypoint(waypoint_delta, instruction.magnitude)
    elif instruction.action in ["n", "s", "e", "w"]:
        wp_lat_delta, wp_long_delta = calculate_direction_deltas(
            instruction.action, instruction.magnitude
        )
        wp_lat, wp_long = waypoint_delta
        waypoint_delta = (wp_lat + wp_lat_delta, wp_long + wp_long_delta)
    else:
        raise AssertionError(f"invalid action '{instruction.action}'")

    return waypoint_delta, lat_delta, long_delta


def partTwo(instr: str) -> int:
    input_list = parse(instr)

    waypoint_delta = (1, 10)
    lat = 0  # north/south, pos/neg
    long = 0  # west/east, pos/neg

    for instruction in input_list:
        waypoint_delta, lad, lod = translate_movement(waypoint_delta, instruction)
        lat += lad
        long += lod

    # Calculate manhattan distance
    # If either value is negative, make it positive
    if lat < 0:
        lat = lat + -2 * lat
    if long < 0:
        long = long + -2 * long

    return lat + long
