from common import *
import copy


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

def find_neighbours(matrix:Matrix3D, raw_point:Tuple[int, int, int]) -> int:
    x, y, z = raw_point
    num_neighbours = 0
    for (vx, vy, vz) in translation_vectors:
        try:
            current_val = matrix[x+vx, y+vy, z+vz]
        except IndexError:
            continue
        if current_val == active:
            num_neighbours += 1
    return num_neighbours

def iterate(matrix:Matrix3D) -> Matrix3D:
    new = copy.deepcopy(matrix)
    sz = len(matrix.master_array)
    sy = len(matrix.master_array[0])
    sx = len(matrix.master_array[0][0])
    for z in range(sz):
        for y in range(sy):
            for x in range(sx):
                neighbours = find_neighbours(matrix, (x, y, z))
                current_state = matrix[x, y, z]
                if (neighbours == 2 or neighbours == 3) and current_state != active:
                    new[x, y, z] = inactive
                elif neighbours == 3 and current_state == inactive:
                    new[x, y, z] = active
    return new


def partOne(instr: str) -> int:

    input_array = [[y for y in x] for x in instr.strip().split("\n")]
    modifier = math.floor(len(input_array) / 2)

    size = (iterations * 2) + 1 + len(input_array)
    print(size)

    m = Matrix3D(size, size, size, default_value=".")
    for y in range(len(input_array)):
        for x in range(len(input_array[y])):
            ux, uy, uz = m.translate(x-modifier, y-modifier, 0)
            m[ux, uy, uz] = input_array[y][x]

    for _ in range(iterations):
        m = iterate(m)

    active_count = 0
    for z in range(len(m.master_array)):
        for y in range(len(m.master_array[0])):
            for x in range(len(m.master_array[0][0])):
                if m[x, y, z] == active:
                    active_count += 1

    return active_count

