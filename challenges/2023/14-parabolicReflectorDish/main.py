import sys
from enum import Enum, auto


def parse(instr: str) -> tuple[str]:
    return tuple(instr.splitlines())


class TiltDirection(Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()


def flip_platform(p: tuple[str]) -> tuple[str]:
    return tuple(map(lambda x: "".join(x), zip(*p)))


def tilt_platform(platform: tuple[str], direction: TiltDirection) -> tuple[str]:
    if direction == TiltDirection.North or direction == TiltDirection.South:
        platform = flip_platform(platform)

    if direction == TiltDirection.North or direction == TiltDirection.West:
        transformation = lambda x: x.replace(".O", "O.")
    else:
        transformation = lambda x: x.replace("O.", ".O")

    res = []

    for line in platform:
        prev = ""
        l = line
        while prev != l:
            prev = l
            l = transformation(l)

        res.append(l)

    if direction == TiltDirection.North or direction == TiltDirection.South:
        res = flip_platform(res)

    return tuple(res)


def calc_north_load(platform: tuple[str]) -> int:
    acc = 0
    for y, line in enumerate(platform):
        for x, char in enumerate(line):
            if char != "O":
                continue
            acc += len(platform) - y
    return acc


def one(instr: str):
    platform = parse(instr)
    platform = tilt_platform(platform, TiltDirection.North)
    return calc_north_load(platform)


def two(instr: str):
    platform = parse(instr)

    ITERS = 1_000_000_000

    i = 0
    known = {}
    jumped = False
    while i < ITERS:
        for direction in [
            TiltDirection.North,
            TiltDirection.West,
            TiltDirection.South,
            TiltDirection.East,
        ]:
            platform = tilt_platform(platform, direction)

        if not jumped:
            if platform in known:
                last_occurrence = known[platform]
                period = i - last_occurrence
                i += ((ITERS - i) // period) * period
                jumped = True
            else:
                known[platform] = i
        i += 1

    return calc_north_load(platform)


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        sys.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))
