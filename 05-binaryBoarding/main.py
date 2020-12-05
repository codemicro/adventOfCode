from typing import Tuple

input_list = open("input.txt").read().strip().split("\n")

front = "F"
back = "B"
left = "L"
right = "R"

num_rows = 128
num_cols = 8

def decode_position(row_string:str, dec_char:str, inc_char:str, max_val:int) -> int:
    min_val = 0
    max_val -= 1

    current_range = (max_val + 1) - min_val
    
    for char in row_string.upper():

        range_modifier = current_range / 2

        if char == dec_char:
            max_val -= range_modifier
        elif char == inc_char:
            min_val += range_modifier

        current_range /= 2

    if row_string[-1] == dec_char:
        return min_val
    else:
        return max_val

def parse_seat(seat_string:str) -> Tuple[int, int]:
    row = decode_position(seat_string[:7], front, back, num_rows)
    col = decode_position(seat_string[7:], left, right, num_cols)

    return int(row), int(col)

def get_seat_id(row:int, col:int) -> int:
    return (row * 8) + col

# --- Part one ---

highest_seat_id = 0
for seat in input_list:
    parsed_seat = parse_seat(seat)
    seat_id = get_seat_id(*parsed_seat)
    if seat_id > highest_seat_id:
        highest_seat_id = seat_id

print(f"Part one: The highest seat ID is {highest_seat_id}.")

# --- Part two ---

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

            print(f"Part two: Your seat ID is {get_seat_id(prev_row, prev_col)} (row {prev_row}, col {prev_col}).")

        lastTwo = lastOne
        lastOne = this
