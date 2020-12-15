from typing import List, Tuple


def find_value_n(instr:str, threshold:int) -> Tuple[int, List[int]]:
    inp = [int(x) for x in instr.strip().split(",")]

    indexes = {}

    for i, n in enumerate(inp):
        indexes[n] = i

    while len(inp) < threshold:
        c = len(inp) - 1
        previous_number = inp[c]

        previous_occurance_index = indexes.get(previous_number, None)
        new_number = 0

        if previous_occurance_index is not None:
            new_number = c - previous_occurance_index

        indexes[previous_number] = c
        
        inp.append(new_number)

    return inp[-1], inp