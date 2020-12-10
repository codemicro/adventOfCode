import copy
import sys
from typing import List, Tuple


class Adaptor:
    output: int
    min_input: int
    max_input: int

    def __init__(self, output_joltage: int) -> None:
        self.output = output_joltage
        self.min_input = output_joltage - 3
        self.max_input = output_joltage - 1

    def is_compatible(self, input_joltage: int) -> bool:
        return (self.min_input <= input_joltage) and (self.max_input >= input_joltage)


def parse(instr: str) -> List[Adaptor]:
    # If I don't sort it, the recusrion in part one takes impossibly long to run
    return sorted(
        [Adaptor(int(x)) for x in instr.strip().split("\n")], key=lambda x: x.output
    )


def find_chain(adaptors: List[Adaptor], current_joltage: int) -> Tuple[bool, int, int]:
    # Returns if found a chain, and a delta for the one diff and three diff

    if len(adaptors) == 0:
        return True, 0, 0

    candidates = [
        (i, a) for i, a in enumerate(adaptors) if a.is_compatible(current_joltage)
    ]

    if len(candidates) == 0:
        return False, 0, 0

    for possible_adaptor in candidates:
        lc = copy.deepcopy(adaptors)
        lc.pop(possible_adaptor[0])

        found_chain, num_one_diff, num_three_diff = find_chain(
            lc, possible_adaptor[1].output
        )

        if found_chain:
            od = 0
            td = 0

            diff = possible_adaptor[1].output - current_joltage
            if diff == 1:
                od += 1
            elif diff == 3:
                td += 1

            return True, od + num_one_diff, td + num_three_diff

    return False, 0, 0


def partOne(instr: str) -> int:
    adaptors = parse(instr)

    # Add device adaptor
    max_j_adaptor = max(adaptors, key=lambda x: x.output)
    adaptors.append(Adaptor(max_j_adaptor.output + 3))

    s, oj, tj = find_chain(adaptors, 0)

    if s:
        return oj * tj
    else:
        return 0
