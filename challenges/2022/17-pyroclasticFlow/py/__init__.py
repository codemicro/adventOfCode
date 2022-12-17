from typing import *
from aocpy import BaseChallenge, Vector, RepeatingConsumer, foldl

Tube = Dict[Vector, None]
Rock = Tuple[int, int, int, int, int]


TUBE_WIDTH = 7

# Coordinate system:
#       ^
#       |
# x --------->
#       |
#       y


def parse_rock(x: str) -> Tuple[Tuple[Vector], Tuple[Vector]]:
    res = []
    for y, line in enumerate(reversed(x.strip().splitlines())):
        for x, char in enumerate(line):
            if char == "#":
                res.append(Vector(x, y))

    height = y + 1
    width = x + 1

    left = []
    right = []
    for y in range(height):
        cx = tuple(coord.x for coord in res if coord.y == y)
        min_x = min(cx)
        max_x = max(cx)

        left.append(Vector(min_x, y))
        right.append(Vector(max_x, y))

    below = []
    for x in range(width):
        min_y = min(coord.y for coord in res if coord.x == x)
        below.append(Vector(x, min_y - 1))

    return tuple(res), tuple(left), tuple(right), tuple(below), width


ROCKS: List[Rock] = [
    parse_rock(lines)
    for lines in "####\n\n.#.\n###\n.#.\n\n..#\n..#\n###\n\n#\n#\n#\n#\n\n##\n##".split(
        "\n\n"
    )
]


def get_num_rows(tube: Tube) -> int:
    filled_spaces = tube.keys()
    return max(x.y for x in filled_spaces) + 1 if len(filled_spaces) != 0 else 0


def get_rock_position(
    rock: Rock, instructions: RepeatingConsumer, tube: Tube
) -> Vector:
    (_, slots_left, slots_right, slots_below, rock_width) = rock

    filled_spaces = tube.keys()
    position = Vector(2, get_num_rows(tube) + 3)

    while True:
        shift_direction = instructions.take()

        delta_x = 0

        if shift_direction == "<":
            if position.x - 1 >= 0:
                delta_x = -1
        elif shift_direction == ">":
            if position.x + rock_width < TUBE_WIDTH:
                # rock_width includes a +1 for our needs
                delta_x = 1
        else:
            raise ValueError("invalid shift direction")

        if delta_x != 0:
            slots = slots_left if delta_x < 0 else slots_right
            can_move = foldl(
                lambda x, y: x and y,
                (
                    ((p.x + position.x + delta_x, p.y + position.y) not in tube)
                    for p in slots
                ),
                True,
            )

            if can_move:
                position.x += delta_x

        can_move_down = False
        if position.y != 0:
            can_move_down = foldl(
                lambda x, y: x and y,
                (
                    ((p.x + position.x, p.y + position.y) not in tube)
                    for p in slots_below
                ),
                True,
            )

        if not can_move_down:
            break

        position.y -= 1

    return position


def add_rock(rock: Rock, position: Vector, tube: Tube):
    rock_shape = rock[0]
    for p in rock_shape:
        tube[Vector(position.x + p.x, position.y + p.y)] = None


def get_row_bitmap(tube: Tube, y: int) -> int:
    n = 0
    for i in range(TUBE_WIDTH):
        n = n << 1
        n += 1 if (i, y) in tube else 0
    return n


def check_for_sequences(tube: Tube) -> Optional[Tuple[int, int]]:
    rows = get_num_rows(tube)

    segment_size = rows // 2

    if segment_size % 100 == 0:
        print(f"starting segment size {segment_size}", flush=True)

    while segment_size > 30:
        possible_positions = (rows - (segment_size * 2)) + 1

        for i in range(possible_positions):
            continuous = True
            for n in range(segment_size):

                for x in range(TUBE_WIDTH):
                    if (x, i + n) in tube != (x, i + n + segment_size) in tube:
                        continuous = False
                        break

                if not continuous:
                    break

            if continuous:
                return segment_size, i

        segment_size -= 1

    return None


def count_rocks_to_height(
    tube: Tube, rocks: RepeatingConsumer, instructions: RepeatingConsumer, height: int
) -> int:
    n = 0
    while get_num_rows(tube) != height:
        rock = rocks.take()
        pos = get_rock_position(rock, instructions, tube)
        add_rock(rock, pos, tube)
        n += 1
    return n


def get_heights(tube: Tube) -> Tuple[Tuple[int], int]:
    max_height = get_num_rows(tube)
    res = []
    for x in range(TUBE_WIDTH):
        largest = 0
        for v in (p.y for p in tube if p.x == x):
            if v > largest:
                largest = v
        res.append(max_height - largest)
    return tuple(res), max_height


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        tube: Tube = {}
        instructions = RepeatingConsumer(instr.strip())
        rocks = RepeatingConsumer(ROCKS)

        for _ in range(2022):
            rock = rocks.take()
            pos = get_rock_position(rock, instructions, tube)
            add_rock(rock, pos, tube)

        return get_num_rows(tube)

    @staticmethod
    def two(instr: str) -> int:
        tube: Tube = {}
        instructions = RepeatingConsumer(instr.strip())
        rocks = RepeatingConsumer(ROCKS)

        seen: Dict[int, int] = {}

        target = 1000000000000

        num_rocks_thrown = 0
        while num_rocks_thrown < target:
            rock = rocks.take()
            pos = get_rock_position(rock, instructions, tube)
            add_rock(rock, pos, tube)

            col_heights, max_height = get_heights(tube)
            h = (rocks.i, instructions.i, *col_heights)
            if h in seen:
                cycle_begins, height_at_cycle_begin = seen[h]

                rocks_thrown_per_cycle = num_rocks_thrown - cycle_begins
                height_increase_per_cycle = max_height - height_at_cycle_begin

                rocks_left_to_throw = target - num_rocks_thrown
                full_cycles_remaining = rocks_left_to_throw // rocks_thrown_per_cycle
                num_rocks_thrown += rocks_thrown_per_cycle * full_cycles_remaining

                # so we don't get any more cache hit while we run through the last few
                seen = {}
            else:
                seen[h] = (num_rocks_thrown, max_height)

            num_rocks_thrown += 1

        return get_num_rows(tube) + (height_increase_per_cycle * full_cycles_remaining)
