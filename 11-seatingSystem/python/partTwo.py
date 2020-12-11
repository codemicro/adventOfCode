from typing import List, Tuple

from common import *


def get_new_state(num_neighbours:int, old_state:str) -> str:
    if num_neighbours == 0:
        return filled_seat
    elif num_neighbours >= 5 and old_state == filled_seat:
        return open_seat

    return old_state


def count_neighbours(hall:List[List[str]], current_pos:Tuple[int, int], hall_size:Tuple[int, int]) -> int:
    num_neighbours = 0 
    deltas = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]

    row, col = current_pos

    for (x, y) in deltas:

        test_x_pos = col + x
        test_y_pos = row + y

        while 0 <= test_x_pos < hall_size[0] and 0 <= test_y_pos < hall_size[1]:

            test_location = hall[test_y_pos][test_x_pos]

            if test_location == filled_seat:
                num_neighbours += 1

            if test_location in [open_seat, filled_seat]:
                break

            test_x_pos += x
            test_y_pos += y

    return num_neighbours


def partTwo(instr: str) -> int:
    return run(parse(instr), count_neighbours, get_new_state)
