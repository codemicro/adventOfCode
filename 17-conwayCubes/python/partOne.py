from common import *
import copy
from pprint import pprint


iterations = 6

translation_vectors = [
    (-1, 1, 1),
    (0, 1, 1),
    (1, 1, 1),
    (-1, 0, 1),
    (0, 0, 1),
    (1, 0, 1),
    (-1, -1, 1),
    (0, -1, 1),
    (1, -1, 1),
    (-1, 1, -1),
    (0, 1, -1),
    (1, 1, -1),
    (-1, 0, -1),
    (0, 0, -1),
    (1, 0, -1),
    (-1, -1, -1),
    (0, -1, -1),
    (1, -1, -1),
    (-1, 1, 0),
    (0, 1, 0),
    (1, 1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (-1, -1, 0),
    (0, -1, 0),
    (1, -1, 0)
]

def find_neighbours(matrix:List[List[List[int]]], raw_point:Tuple[int, int, int]) -> int:
    x, y, z = raw_point
    num_neighbours = 0
    for (vx, vy, vz) in translation_vectors:
        vx += x
        vy += y
        vz += z

        if vx < 0 or vy < 0 or vz < 0:
            continue

        try:
            current_val = matrix[vz][vy][vx]
        except IndexError:
            continue

        if current_val == active:
            num_neighbours += 1
    return num_neighbours

def iterate(matrix:List[List[List[int]]]) -> List[List[List[int]]]:
    new = copy.deepcopy(matrix)
    sz = len(matrix)
    sy = len(matrix[0])
    sx = len(matrix[0][0])
    for z in range(sz):
        for y in range(sy):
            for x in range(sx):
                neighbours = find_neighbours(matrix, (x, y, z))
                current_state = matrix[z][y][x]
                if (neighbours == 2 or neighbours == 3) and current_state != active:
                    new[z][x][y] = inactive
                elif neighbours == 3 and current_state == inactive:
                    new[z][x][y] = active
    return new


def partOne(instr: str) -> int:

    input_array = [[y for y in x] for x in instr.strip().split("\n")]

    assert len(input_array) == len(input_array[0]), "input array must be square"
    input_size = len(input_array)

    # determine matrix size and create
    size = (iterations * 2) + 1 + len(input_array) # 1 extra col/row/whatever around per iteration
    if size % 2 != len(input_array) % 2:
        size += 1 # the len and size must both be even or odd
    matrix = [[[inactive for _ in range(size)] for _ in range(size)] for _ in range(size)]

    # Load input into center of matrix
    centerpoint = size / 2
    centerpoint_mod = len(input_array) / 2
    start_point = int((centerpoint - centerpoint_mod) - 1)

    center_z = int(size / 2) - 1

    for y in range(input_size):
        for x in range(input_size):
            matrix[center_z][y + start_point][x + start_point] = input_array[y][x]

    # Iterate
    for _ in range(iterations):
        matrix = iterate(matrix)

    # Count active
    active_count = 0

    sz = len(matrix)
    sy = len(matrix[0])
    sx = len(matrix[0][0])
    for z in range(sz):
        for y in range(sy):
            for x in range(sx):
                if matrix[z][y][x] == active:
                    active_count += 1

    return active_count

