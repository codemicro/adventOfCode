from typing import Dict, Tuple, Callable
import itertools


active_marker = "#"
inactive_marker = "."


translation_vectors_3d = [
    p for p in itertools.product([-1, 0, 1], repeat=3) if p != (0, 0, 0)
]
translation_vectors_4d = [
    p for p in itertools.product([-1, 0, 1], repeat=4) if p != (0, 0, 0, 0)
]


def parse(
    instr: str, key: Callable[[int, int], int]
) -> Dict[Tuple[int, int, int], str]:
    input_lists = [[x for x in y] for y in instr.strip().split("\n")]

    rtvl = {}

    for y, row in enumerate(input_lists):
        for x, col in enumerate(row):
            if col != inactive_marker:
                rtvl[key(x, y)] = col

    return rtvl
