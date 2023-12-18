import sys
import re
from collections import namedtuple
import gridutil.coord as cu
import gridutil.grid as gu


Instruction = namedtuple("Instruction", ["direction", "dist", "colour"])
PARSE_RE = re.compile(r"([RDUL]) (\d+) \(#([a-f\d]{6})\)")
DIRECTION_TRANSFORMATION = {
    "R": cu.Direction.Right,
    "L": cu.Direction.Left,
    "U": cu.Direction.Up,
    "D": cu.Direction.Down,
    "0": cu.Direction.Right,
    "1": cu.Direction.Down,
    "2": cu.Direction.Left,
    "3": cu.Direction.Up,
}


def parse(instr: str) -> list[Instruction]:
    res = []
    for line in instr.splitlines():
        m = PARSE_RE.match(line)
        assert m is not None

        raw_dir, dist, colour = m.groups()
        parsed_dir = DIRECTION_TRANSFORMATION[raw_dir]
        assert parsed_dir is not None

        res.append(Instruction(parsed_dir, int(dist), colour))
    return res


def run(instructions: list[Instruction]) -> int:
    perimeter = 0
    vertices = [cu.Coordinate(0, 0)]
    for instruction in instructions:
        perimeter += instruction.dist
        vertices.append(
            cu.add(
                vertices[-1], cu.mult(instruction.direction.delta(), instruction.dist)
            )
        )

    vertices = vertices[:-1]

    area = cu.area(vertices)

    # This is Pick's theorem.
    # Normally, we'd want to just get the internal area, which the Shoelace formula would do.
    # But since we want the area including walls that we assume are a single
    # unit thick, we apply Pick's theorem as this counts all coordinates that
    # the walls pass through, which in this case is effectively the same thing.
    return int(area + perimeter / 2) + 1


def one(instr: str):
    instructions = parse(instr)
    return run(instructions)


def two(instr: str):
    instructions = parse(instr)
    for i, instruction in enumerate(instructions):
        instructions[i] = Instruction(
            DIRECTION_TRANSFORMATION[instruction.colour[-1]],
            int(instruction.colour[:5], base=16),
            "",
        )
    return run(instructions)


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
