from typing import Dict, List, Tuple
from aocpy import BaseChallenge


LIT = "#"
UNLIT = "."


Point = Tuple[int, int]
Image = Dict[Point, str]


def parse(instr: str) -> Tuple[str, Image]:
    algo, image = instr.strip().split("\n\n")

    image_dict = {}

    for y, line in enumerate(image.splitlines()):
        for x, char in enumerate(line):
            if char == LIT:
                image_dict[(x, y)] = char

    return algo, image_dict


def get_adjacent_points(center_point: Point) -> List[Point]:
    x, y = center_point
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]


def enhance_n(image: Image, algorithm: str, n: int):
    # one does not simply "enhance" the image...

    for i in range(n):
        min_x = min(x for x, _ in image)
        max_x = max(x for x, _ in image)
        min_y = min(y for _, y in image)
        max_y = max(y for _, y in image)

        changes = {}
        for y in range(min_y - 2, max_y + 3):
            for x in range(min_x - 2, max_x + 3):
                p = (x, y)

                n = 0
                for point in get_adjacent_points(p):
                    px, py = point

                    is_lit = False

                    # If the first component of the algorithm (the one that's
                    # used when no lit pixels are present) is lit, we can
                    # assume that on every other iteration, the infinite dim
                    # pixels are going to alternate between being lit and dim,
                    # hence this weirdness.

                    if algorithm[0] == LIT and not (
                        min_x <= px <= max_x and min_y <= py <= max_y
                    ):
                        is_lit = i % 2 != 0
                    else:
                        is_lit = image.get(point, UNLIT) == LIT

                    n = (n << 1) | (0b1 if is_lit else 0b0)

                changes[p] = algorithm[n]

        for point in changes:
            change = changes[point]
            if change == UNLIT and point in image:
                del image[point]
            elif change == LIT:
                image[point] = LIT


class Challenge(BaseChallenge):
    @staticmethod
    def core(instr: str, n: int) -> int:
        algorithm, image = parse(instr)
        enhance_n(image, algorithm, n)
        return len(image)  # only lit pixels are included

    @staticmethod
    def one(instr: str) -> int:
        return Challenge.core(instr, 2)

    @staticmethod
    def two(instr: str) -> int:
        return Challenge.core(instr, 50)
