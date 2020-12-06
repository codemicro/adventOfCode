from common import *


def partOne(instr: str) -> int:
    input_list = parse(instr)

    highest_seat_id = 0
    for seat in input_list:
        parsed_seat = parse_seat(seat)
        seat_id = get_seat_id(*parsed_seat)
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id

    return highest_seat_id
