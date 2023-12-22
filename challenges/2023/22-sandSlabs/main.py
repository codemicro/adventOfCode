import sys
import gridutil.coord as cu
from tqdm import tqdm


Brick = tuple[cu.Coordinate3, cu.Coordinate3]


def parse(instr: str) -> set[Brick]:
    # (sorry)
    return set(
        sorted(
            [
                tuple(
                    sorted(
                        map(
                            lambda x: cu.Coordinate3(*map(int, x.split(","))),
                            line.split("~"),
                        )
                    )
                )
                for line in instr.splitlines()
            ],
            key=lambda x: x[0].z,
        )
    )


def are_bricks_overlapping(a: Brick, b: Brick) -> bool:
    x_overlaps = a[0].x <= b[1].x and b[0].x <= a[1].x
    y_overlaps = a[0].y <= b[1].y and b[0].y <= a[1].y
    return x_overlaps and y_overlaps


def lower_bricks(
    bricks: set[Brick], start_at: int = 2, return_early: bool = False
) -> int:
    max_z = max([x[1].z for x in bricks]) + 1
    n = 0
    for level in range(start_at, max_z if not return_early else start_at + 1):
        present_below = []
        on_this_level = []

        for brick in bricks:
            if brick[1].z == level - 1:
                present_below.append(brick)
            elif brick[0].z == level:
                on_this_level.append(brick)

        for brick in on_this_level:
            overlaps = False
            for lower_brick in present_below:
                if are_bricks_overlapping(brick, lower_brick):
                    overlaps = True
                    break

            if not overlaps:
                n += 1
                # This is what lowering a brick looks like
                bricks.remove(brick)
                bricks.add(
                    (
                        cu.Coordinate3(brick[0].x, brick[0].y, brick[0].z - 1),
                        cu.Coordinate3(brick[1].x, brick[1].y, brick[1].z - 1),
                    )
                )

    return n


def collapse_tower(bricks: set[Brick]):
    changed = 1
    while changed != 0:
        changed = lower_bricks(bricks)


def generate_openscad(bricks: set[Brick]) -> str:
    """
    This was for debugging
    """
    lines = []
    for brick in bricks:
        lines.append(
            "translate(["
            + (", ".join(map(str, brick[0])))
            + "]) { cube(["
            + (
                ", ".join(
                    map(str, map(lambda x: 1 + brick[1][x] - brick[0][x], range(3)))
                )
            )
            + "], center=false); };"
        )
    return "\n".join(lines)


def one(instr: str):
    bricks = parse(instr)

    _debug("Building initial state", end="\r")

    collapse_tower(bricks)

    acc = 0
    for brick in tqdm(bricks, desc="Testing individual bricks", file=sys.stderr, leave=False):
        bc = bricks.copy()
        bc.remove(brick)
        v = lower_bricks(bc, start_at=brick[1].z + 1, return_early=True)
        if v == 0:
            acc += 1

    return acc


def two(instr: str):
    bricks = parse(instr)

    _debug("Building initial state", end="\r")

    collapse_tower(bricks)

    acc = 0
    for brick in tqdm(bricks, desc="Testing individual bricks", file=sys.stderr, leave=False):
        bc = bricks.copy()
        bc.remove(brick)
        v = lower_bricks(bc, start_at=brick[1].z + 1)
        if v != 0:
            acc += v

    return acc


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
