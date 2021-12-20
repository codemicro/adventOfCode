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

    @staticmethod
    def vis(instr: str, output_dir: str):
        from PIL import Image
        import os
        import subprocess
        import sys
        from aocpy.vis import SaveManager
        import shutil
        import copy
        import io

        COLOUR_BACKGROUND = tuple(bytes.fromhex("FFFFFF"))
        COLOUR_DIM = tuple(bytes.fromhex("05445E"))
        COLOUR_LIT = tuple(bytes.fromhex("189AB4"))

        print("Generating data", flush=True)

        algorithm, image = parse(instr)
        images = []
        for _ in range(50):
            images.append(copy.copy(image))
            enhance_n(image, algorithm, 1)

        print("Generating frames", flush=True)

        min_x = min(x for x, _ in image)
        max_x = max(x for x, _ in image)
        min_y = min(y for _, y in image)
        max_y = max(y for _, y in image)

        range_x = max_x - min_x
        range_y = max_y - min_y

        offset_x = -min_x
        offset_y = -min_y

        temp_dir = os.path.join(output_dir, "vis-temp")
        try:
            os.makedirs(temp_dir)
        except FileExistsError:
            pass

        manager = SaveManager(temp_dir)

        for frame in images:
            img = Image.new("RGB", (range_x + 1, range_y + 1), COLOUR_DIM)
            for pixel in frame:
                x, y = pixel
                img.putpixel((x + offset_x, y + offset_y), COLOUR_LIT)
            manager.save(img)

        print("Encoding frames", flush=True)

        output_file = f"{output_dir}/out.mp4"

        try:
            os.remove(output_file)
        except FileNotFoundError:
            pass

        subprocess.call(
            ["ffmpeg", "-framerate", "5", "-i", f"{output_dir}/vis-temp/frame_%04d.png", "-start_number", "0", "-c:v", "libx264", "-vf", "scale=iw*5:ih*5:flags=neighbor", "-r", "30", "-pix_fmt", "yuv420p", output_file],
            stdout=sys.stdout,
            stderr=subprocess.STDOUT,
        )

        print("Tidying up", flush=True)

        shutil.rmtree(temp_dir)
