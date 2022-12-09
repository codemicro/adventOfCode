from typing import *
from aocpy import BaseChallenge

Vector = Tuple[int, int]
Instruction = Tuple[str, int]

LEFT = "L"
RIGHT = "R"
UP = "U"
DOWN = "D"

OFFSETS = {
    RIGHT: (1, 0),
    LEFT: (-1, 0),
    UP: (0, 1),
    DOWN: (0, -1),
}


def parse(instr: str) -> List[Instruction]:
    return [(x[0], int(x[2:])) for x in instr.strip().splitlines()]


def vector_sum(a: Vector, b: Vector) -> Vector:
    return (a[0] + b[0], a[1] + b[1])


def vector_diff(a: Vector, b: Vector) -> Vector:
    return (a[0] - b[0], a[1] - b[1])


def get_next_move_delta(
    current_position: Vector, preceeding_position: Vector
) -> Optional[Vector]:
    (dx, dy) = vector_diff(preceeding_position, current_position)

    if -1 <= dx <= 1 and -1 <= dy <= 1:
        return None

    if dy > 0 and dx == 0:
        # head upwards of tail
        return OFFSETS[UP]
    elif dy < 0 and dx == 0:
        # head downwards of tail
        return OFFSETS[DOWN]
    elif dy == 0 and dx > 0:
        # head to the right of tail
        return OFFSETS[RIGHT]
    elif dy == 0 and dx < 0:
        # head to the left of tail
        return OFFSETS[LEFT]
    elif dy > 0 and dx > 0:
        # head diagonally up-right of the tail
        return vector_sum(OFFSETS[UP], OFFSETS[RIGHT])
    elif dy > 0 and dx < 0:
        # head diagonally up-left of the tail
        return vector_sum(OFFSETS[UP], OFFSETS[LEFT])
    elif dy < 0 and dx > 0:
        # head diagonally down-right of the tail
        return vector_sum(OFFSETS[DOWN], OFFSETS[RIGHT])
    elif dy < 0 and dx < 0:
        # head diagonally down-left of the tail
        return vector_sum(OFFSETS[DOWN], OFFSETS[LEFT])

    return None


def run_with_length(instructions: List[Instruction], length: int) -> int:
    tail_visited: List[Vector] = [(0, 0)]

    positions: List[Vector] = [(0, 0) for _ in range(length)]

    for (direction, magnitude) in instructions:
        for _ in range(magnitude):
            positions[0] = vector_sum(positions[0], OFFSETS[direction])

            for pos_num in range(1, len(positions)):
                delta = get_next_move_delta(positions[pos_num], positions[pos_num - 1])
                if delta is None:
                    break

                positions[pos_num] = vector_sum(positions[pos_num], delta)

            if delta is None:
                # Python scope nastiness coming in useful for once
                continue

            if positions[-1] not in tail_visited:
                tail_visited.append(positions[-1])

    return len(tail_visited)


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        return run_with_length(parse(instr), 2)

    @staticmethod
    def two(instr: str) -> int:
        return run_with_length(parse(instr), 10)
