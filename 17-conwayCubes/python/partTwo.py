from common import *


def count_neighbours(matrix:Dict[Tuple[int, int, int, int], str], position:Tuple[int, int, int, int]) -> int:
    num_neighbours = 0
    x, y, z, w = position
    for (x_delta, y_delta, z_delta, w_delta) in translation_vectors_4d:
        if matrix.get((x + x_delta, y+y_delta, z+z_delta, w+w_delta), inactive_marker) == active_marker:
            num_neighbours += 1
    return num_neighbours


def iterate(matrix:Dict[Tuple[int, int, int], str]) -> Dict[Tuple[int, int, int], str]:
    new = {}

    # get min/max for x, y and z values
    keys = list(matrix)
    _, _, _, min_w = min(keys, key=lambda x: x[3])
    _, _, _, max_w = max(keys, key=lambda x: x[3])
    _, _, min_z, _ = min(keys, key=lambda x: x[2])
    _, _, max_z, _ = max(keys, key=lambda x: x[2])
    _, min_y, _, _ = min(keys, key=lambda x: x[1])
    _, max_y, _, _ = max(keys, key=lambda x: x[1])
    min_x, _, _, _ = min(keys, key=lambda x: x[0])
    max_x, _, _, _ = max(keys, key=lambda x: x[0])

    for w in range(min_w - 2, max_w + 2):
        for z in range(min_z - 2, max_z + 2):
            for y in range(min_y - 2, max_y + 2):
                for x in range(min_x - 2, max_x + 2):
                    num_neighbours = count_neighbours(matrix, (x, y, z, w))
                    current_state = matrix.get((x, y, z, w), inactive_marker)
                    if (num_neighbours == 2 and current_state == active_marker) or num_neighbours == 3:
                        new[(x, y, z, w)] = active_marker

    return new


def partTwo(instr: str) -> int:
    matrix = parse(instr, lambda x, y: (x, y, 0, 0))
    
    for _ in range(6):
        matrix = iterate(matrix)

    return len(matrix)
