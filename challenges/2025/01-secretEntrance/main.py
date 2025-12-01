import sys


LEFT = "L"
RIGHT = "R"


def parse(instr: str) -> list[tuple[str, int]]:
    return list(map(lambda x: (x[0], int(x[1:])), instr.splitlines()))


def one(instr: str):
    parsed = parse(instr)

    n = 0
    wheel = 50
    for (direction, distance) in parsed:
        if direction == LEFT:
            distance = -distance
        
        wheel += distance
        if wheel % 100 == 0:
            n += 1

    return n


def two(instr: str):
    parsed = parse(instr)
    
    n = 0
    wheel = 50

    for (direction, distance) in parsed:
        delta = 1
        if direction == LEFT:
            delta = -1

        for _ in range(distance):
            wheel += delta
            wheel = wheel % 100
            if wheel == 0:
                n += 1

    return n


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