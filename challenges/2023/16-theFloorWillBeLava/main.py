import gridutil.grid as gu
import gridutil.coord as cu
from enum import Enum, auto
import sys
from collections import defaultdict


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


DIRECTION_DELTAS = {
    Direction.Up: (0, -1),
    Direction.Down: (0, 1),
    Direction.Left: (-1, 0),
    Direction.Right: (1, 0),
}


def parse(instr: str) -> gu.Grid:
    return gu.parse(instr)


def get_n_energised(
    box: gu.Grid, start_pos: cu.Coordinate, start_directon: Direction
) -> int:
    energised = defaultdict(lambda: [])
    beams = [(start_pos, start_directon)]

    while beams:
        (pos, direction) = beams.pop(0)

        while True:
            if pos not in box:
                break

            if pos in energised and direction in energised[pos]:
                break
            else:
                energised[pos].append(direction)

            at_pos = box[pos]

            match at_pos:
                case "/":
                    match direction:
                        case Direction.Up:
                            direction = Direction.Right
                        case Direction.Down:
                            direction = Direction.Left
                        case Direction.Left:
                            direction = Direction.Down
                        case Direction.Right:
                            direction = Direction.Up

                case "\\":
                    match direction:
                        case Direction.Up:
                            direction = Direction.Left
                        case Direction.Down:
                            direction = Direction.Right
                        case Direction.Left:
                            direction = Direction.Up
                        case Direction.Right:
                            direction = Direction.Down

                case "-":
                    if not (
                        direction == Direction.Left or direction == direction.Right
                    ):
                        beams.append(
                            (
                                (cu.add(pos, DIRECTION_DELTAS[Direction.Left])),
                                Direction.Left,
                            )
                        )
                        direction = Direction.Right

                case "|":
                    if not (direction == Direction.Up or direction == direction.Down):
                        beams.append(
                            (
                                (cu.add(pos, DIRECTION_DELTAS[Direction.Up])),
                                Direction.Up,
                            )
                        )
                        direction = Direction.Down

            pos = cu.add(pos, DIRECTION_DELTAS[direction])

    return len(energised)


def one(instr: str):
    box = parse(instr)
    return get_n_energised(box, (0, 0), Direction.Right)


def two(instr: str):
    box = parse(instr)

    max_x = gu.get_max_x(box)
    max_y = gu.get_max_y(box)

    starts = [(0, y) for y in range(max_y + 1)]
    starts += [(max_x, y) for y in range(max_y + 1)]
    starts += [(x, 0) for x in range(1, max_x)]
    starts += [(x, max_y) for x in range(1, max_x)]

    max_energised = 0

    for start in starts:
        for direction in Direction:
            x = get_n_energised(box, start, direction)
            if x > max_energised:
                max_energised = x

    return max_energised


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
