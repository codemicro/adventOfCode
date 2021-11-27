from common import *
from partOne import partOne


def partTwo(instr: str) -> int:
    input_list = parse(instr)

    target_value = partOne(instr)
    if target_value == 0:
        return 0

    pointer = 0
    while pointer < len(input_list):
        # iterate consecutive values from here
        start_point = pointer
        iptr = pointer  # Internal PoinTeR
        count = 0
        while iptr < len(input_list):
            count += input_list[iptr]

            if count == target_value:
                # must be at least two values
                if iptr - start_point < 2:
                    break

                all_values = input_list[start_point : iptr + 1]
                return min(all_values) + max(all_values)

            if count > target_value:
                break

            iptr += 1

        pointer += 1

    return 0
