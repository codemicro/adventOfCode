from common import *


def partTwo(instr: str) -> int:
    input_list = parse(instr)

    # Build a matrix to represent the entire plane
    # False represents an empty seat
    seat_matrix = []
    for _ in range(num_rows):
        x = []
        for _ in range(num_cols):
            x.append(False)
        seat_matrix.append(x)

    # Populate that matrix
    for seat in input_list:
        row, col = parse_seat(seat)
        seat_matrix[row][col] = True

    lastOne = None
    lastTwo = None

    for row in range(len(seat_matrix)):
        for col in range(len(seat_matrix[row])):

            this = seat_matrix[row][col]
            if [lastTwo, lastOne, this] == [True, False, True]:

                # We need to get the previous item because at this point, we've already moved on one
                prev_row = row
                prev_col = col - 1
                if prev_col < 0:
                    prev_row -= 1

                return get_seat_id(prev_row, prev_col)

            lastTwo = lastOne
            lastOne = this

    return 0
