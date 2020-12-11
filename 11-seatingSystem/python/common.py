import copy
import time
from typing import Callable, List


open_seat = "L"
filled_seat = "#"
no_seat = "."


def parse(instr: str) -> List[List[str]]:
    return [[char for char in x] for x in instr.strip().split("\n")]

def iterate(current_hall: List[List[str]], neighbour_counter: Callable, get_new_state: Callable) -> List[List[str]]:
    # Copy hall
    next_hall = copy.deepcopy(current_hall) # this is bloody slow

    hall_size = (len(next_hall[0]), len(next_hall))

    # Iterate each chair space
    for col in range(hall_size[0]):
        for row in range(hall_size[1]):
            current_pos = current_hall[row][col]

            # If it's the floor, there's nothing we can do with this spot
            if current_pos == no_seat:
                continue

            # Count number of adjacent seats
            num_neighbours = neighbour_counter(current_hall, (row, col), hall_size)

            # Execute rules on copied list based on that count
            next_hall[row][col] = get_new_state(num_neighbours, next_hall[row][col])

    # Return copied list
    return next_hall

def run(current_state:List[List[str]], neighbour_counter:Callable, get_new_state:Callable) -> int:
    last_state = None

    while current_state != last_state:
        last_state = current_state
        current_state = iterate(current_state, neighbour_counter, get_new_state)

    # at this point, we've ended up with two identical seating arrangements
    # let's count the number of occupied seats
    total_occupied = 0
    for a in current_state:
        for b in a:
            if b == filled_seat:
                total_occupied += 1
    
    return total_occupied