from typing import List, Tuple

front = "F"
back = "B"
left = "L"
right = "R"

num_rows = 128
num_cols = 8

def parse(instr:str) -> List:
    return instr.strip().split("\n")

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
