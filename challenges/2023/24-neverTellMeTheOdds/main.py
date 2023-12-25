import sys
from collections import namedtuple
from numbers import Number
import gridutil.coord as cu
from functools import reduce
import math
import z3


Hailstone = namedtuple("Hailstone", ["position", "velocity"])


def parse(instr: str) -> list[Hailstone]:
    return [
        Hailstone(
            *map(lambda x: cu.Coordinate3(*map(int, x.split(", "))), line.split(" @ "))
        )
        for line in instr.splitlines()
    ]


def get_2d_line(stone: Hailstone) -> tuple[Number, Number]:
    m = stone.velocity.y / stone.velocity.x
    c = stone.position.y - (m * stone.position.x)
    return m, c


def get_2d_intersection(a: Hailstone, b: Hailstone) -> cu.Coordinate | None:
    m1, c1 = get_2d_line(a)
    m2, c2 = get_2d_line(b)

    if math.isclose(m1, m2):
        return None

    x = (c2 - c1) / (m1 - m2)
    y = (m1 * x) + c1
    return cu.Coordinate(x, y)


def one(instr: str):
    hailstones = parse(instr)

    MIN, MAX = (7, 27) if len(hailstones) == 5 else (200000000000000, 400000000000000)

    acc = 0
    for i, stone1 in enumerate(hailstones[:-1]):
        for stone2 in hailstones[i + 1 :]:
            if stone1 == stone2:
                continue

            p = get_2d_intersection(stone1, stone2)
            if p is None or not reduce(lambda acc, x: acc and MIN <= x <= MAX, p, True):
                continue

            if not (
                (p.x > stone1.position.x) == (stone1.velocity.x > 0)
                and (p.x > stone2.position.x) == (stone2.velocity.x > 0)
            ):
                continue
            acc += 1

    return acc


def two(instr: str):
    hailstones = parse(instr)

    # for our thrown rock
    #     initial position: x,  y,  z
    #     velocity:         vx, vy, vz

    # for each of 3 hailstones
    #     time of collision with that hailstone: t_i
    #     intial position:                       hx,  hy,  hz
    #     velocity:                              hvx, hvy, hvz

    x, y, z = (z3.Int(x) for x in ["x", "y", "z"])
    vx, vy, vz = (z3.Int(x) for x in ["vx", "vy", "vz"])

    solver = z3.Solver()

    for i in range(3):
        hailstone = hailstones[i]
        t = z3.Int(f"t_{i}")
        solver.add(
            t >= 0,
            x + (vx * t) == hailstone.position.x + (hailstone.velocity.x * t),
            y + (vy * t) == hailstone.position.y + (hailstone.velocity.y * t),
            z + (vz * t) == hailstone.position.z + (hailstone.velocity.z * t),
        )

    _debug("Solving...", end="", flush=True)
    assert solver.check() == z3.sat
    model = solver.model()
    _debug("\r            \r" + str(model))
    return sum(model[var].as_long() for var in [x, y, z])


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
