from typing import List, Dict, Tuple
from aocpy import BaseChallenge, foldl


Point = Tuple[int, int]
Cave = Dict[Point, int]
Basin = List[Point]


def parse(instr: str) -> Cave:
    o = {}
    for y, line in enumerate(instr.strip().splitlines()):
        for x, digit in enumerate(line):
            o[(x, y)] = int(digit)
    return o


def find_adjacent_points(cave: Cave, position: Point) -> List[Point]:
    # Returns a list of points that are horizontally or vertically adjacent to
    # `point` that exist within `cave`.

    #            (x, y+1)
    #  (x-1, y)  (x, y)    (x+1, y)
    #            (x, y-1)
    #

    x, y = position
    return [
        pos for pos in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)] if pos in cave
    ]


def find_adjacent_heights(cave: Cave, position: Point) -> List[int]:
    # Returns a list of heights of points horizontally or vertically adjacent to
    # `point`

    return [cave[pos] for pos in find_adjacent_points(cave, position) if pos in cave]


def find_low_points(cave: Cave) -> List[Point]:
    # Retusn a list of points in `cave` where all adjacent points are higher
    # than the current point under inspection.

    o = []
    for position in cave:
        height = cave[position]
        are_adjacent_heights_higher = [
            height < adjacent for adjacent in find_adjacent_heights(cave, position)
        ]
        if False not in are_adjacent_heights_higher:
            o.append(position)
    return o


def find_points_in_basin(cave: Cave, low_point: Point) -> List[Point]:
    # Returns a list of points that belong to the basin in `cave` that's
    # centered around `low_point`

    queue = find_adjacent_points(cave, low_point)
    points = [low_point]

    while len(queue) != 0:
        point = queue.pop(0)

        if cave[point] == 9:
            continue

        points.append(point)
        for adjacent in find_adjacent_points(cave, point):
            if adjacent in queue or adjacent in points:
                continue
            queue.append(adjacent)

    return points


def find_basins(cave: Cave) -> List[Basin]:
    # Returns all the basins that exist within `cave`

    low_points = find_low_points(cave)
    basins = []
    for point in low_points:
        basins.append(find_points_in_basin(cave, point))
    return basins


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        cave = parse(instr)

        cumulative_risk_level = 0
        for low_point in find_low_points(cave):
            cumulative_risk_level += cave[low_point] + 1

        return cumulative_risk_level

    @staticmethod
    def two(instr: str) -> int:
        cave = parse(instr)
        basins = find_basins(cave)

        # reverse == descending order
        basins = list(sorted(basins, key=lambda x: len(x), reverse=True))

        return foldl(lambda x, y: x * len(y), basins[0:3], 1)

    @staticmethod
    def vis(instr: str, outputDir: str):
        from PIL import Image, ImageDraw
        import os
        from aocpy.vis import SaveManager
        import shutil

        COLOUR_BACKGROUND = tuple(bytes.fromhex("FFFFFF"))
        COLOUR_SCANNING = tuple(bytes.fromhex("D4F1F4"))
        COLOUR_LOW_POINT = tuple(bytes.fromhex("05445E"))
        COLOUR_BORDER = tuple(bytes.fromhex("189AB4"))
        COLOUR_BASIN = tuple(bytes.fromhex("75E6DA"))

        cave = parse(instr)

        max_x = max(x for x, _ in cave)
        max_y = max(y for _, y in cave)

        img = Image.new("RGB", (max_x + 1, max_y + 1), COLOUR_BACKGROUND)

        temp_dir = os.path.join(outputDir, "vis-temp")
        try:
            os.makedirs(temp_dir)
        except FileExistsError:
            pass

        manager = SaveManager(temp_dir)

        # now we reimplement bits of the challenge

        def find_points_in_basin(cave: Cave, low_point: Point) -> List[Point]:
            queue = find_adjacent_points(cave, low_point)
            points = [low_point]

            while len(queue) != 0:
                point = queue.pop(0)

                if cave[point] == 9:
                    img.putpixel(point, COLOUR_BORDER)
                    manager.save(img)
                    continue

                points.append(point)
                img.putpixel(point, COLOUR_BASIN)
                manager.save(img)
                for adjacent in find_adjacent_points(cave, point):
                    if adjacent in queue or adjacent in points:
                        continue
                    queue.append(adjacent)

            return points

        def find_low_points(cave: Cave) -> List[Point]:
            o = []
            for position in cave:
                img.putpixel(position, COLOUR_SCANNING)
                manager.save(img)

                height = cave[position]
                are_adjacent_heights_higher = [
                    height < adjacent
                    for adjacent in find_adjacent_heights(cave, position)
                ]
                if False not in are_adjacent_heights_higher:
                    o.append(position)
                    img.putpixel(position, COLOUR_LOW_POINT)
                else:
                    img.putpixel(position, COLOUR_BACKGROUND)
            manager.save(img)
            return o

        # actual challenge run
        low_points = find_low_points(cave)
        for point in low_points:
            find_points_in_basin(cave, point)

        os.system(
            f"""ffmpeg -framerate 480 -i {outputDir}/vis-temp/frame_%04d.png -start_number 0 -c:v libx264 -vf "scale=iw*5:ih*5:flags=neighbor" -r 30 -pix_fmt yuv420p {outputDir}/out.mp4"""
        )
        shutil.rmtree(temp_dir)
