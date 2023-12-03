import os
import sys


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


Coordinate = tuple[int, int]
Schematic = dict[Coordinate, str]


def parse(instr: str) -> Schematic:
    res = {}

    lines = instr.splitlines()
    max_x = len(lines[0])

    for row_n, row in enumerate(lines):
        assert len(row) == max_x
        for col_n, char in enumerate(row):
            res[(col_n, row_n)] = char

    return res


DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def apply_coord_delta(c: Coordinate, d: Coordinate) -> Coordinate:
    a, b = c
    e, f = d
    return a + e, b + f


def seek_digits(
    sc: Schematic, start: Coordinate, delta: Coordinate
) -> tuple[str, set[Coordinate]]:
    digits = ""
    coords = set()

    cursor = start
    while True:
        cursor = apply_coord_delta(cursor, delta)
        val = sc.get(cursor, ".")
        if not val.isdigit():
            break
        coords.add(cursor)
        digits += val

    return digits, coords


def collect_digits_around(
    sc: Schematic, start: Coordinate
) -> tuple[int, set[Coordinate]]:
    backward_digits, backward_coords = seek_digits(sc, start, (-1, 0))
    forward_digits, forward_coords = seek_digits(sc, start, (1, 0))

    return (
        int("".join(reversed(backward_digits)) + sc[start] + forward_digits),
        backward_coords | forward_coords | set((start,)),
    )


def one(inp: str):
    schematic = parse(inp)

    consumed_numbers = set()
    acc = 0

    for coord in schematic:
        if coord in consumed_numbers:
            continue

        char = schematic[coord]

        if not char.isdigit():
            continue

        is_part_number = False
        for delta in DIRECTIONS:
            target = schematic.get(apply_coord_delta(coord, delta), ".")
            if not (target.isdigit() or target == "."):
                is_part_number = True
                break

        if is_part_number:
            n, used_coords = collect_digits_around(schematic, coord)
            consumed_numbers = consumed_numbers | used_coords
            acc += int(n)

    return acc


def two(inp: str):
    schematic = parse(inp)
    acc = 0

    for coord in schematic:
        char = schematic[coord]

        if char != "*":
            continue

        consumed_numbers = set()
        numbers = []

        for delta in DIRECTIONS:
            test_coord = apply_coord_delta(coord, delta)
            if test_coord in consumed_numbers:
                continue
            if schematic.get(test_coord, ".").isdigit():
                n, c = collect_digits_around(schematic, test_coord)
                consumed_numbers = consumed_numbers | c
                numbers.append(n)

        if len(numbers) == 2:
            # is gear!
            x, y = numbers
            acc += x * y

    return acc


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        os.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))
