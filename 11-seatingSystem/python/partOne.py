from typing import List, Tuple

from common import *


def get_new_state(num_neighbours: int, old_state: str) -> str:
    if num_neighbours == 0:
        return filled_seat
    elif num_neighbours >= 4 and old_state == filled_seat:
        return open_seat

    return old_state


def count_neighbours(
    hall: List[List[str]], current_pos: Tuple[int, int], hall_size: Tuple[int, int]
) -> int:
    num_neighbours = 0

    row, col = current_pos

    for (x, y) in lookup_positions:
        test_x_pos = x + col
        test_y_pos = y + row

        if 0 <= test_x_pos < hall_size[0] and 0 <= test_y_pos < hall_size[1]:
            if hall[test_y_pos][test_x_pos] == filled_seat:
                num_neighbours += 1

    return num_neighbours


def partOne(instr: str) -> int:
    return run(parse(instr), count_neighbours, get_new_state)
