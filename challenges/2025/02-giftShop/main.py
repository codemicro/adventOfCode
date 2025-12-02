import sys


def parse(instr: str) -> list[tuple[int, int]]:
    return list(
        zip(
            (p := tuple(map(int, instr.replace("-", ",").split(","))))[::2],
            p[1::2],
        ),
    )


def is_repeated_once(n: int) -> bool:
    nstr = str(n)
    if len(nstr) % 2 != 0:
        return False
    midpoint = int(len(nstr) / 2)
    return nstr[:midpoint] == nstr[midpoint:]


def one(instr: str) -> int:
    parsed = parse(instr)
    n = 0
    for (start, end) in parsed:
        for i in range(start, end + 1):
            if is_repeated_once(i):
                n += i
    return n


def has_repeated_segments(n: int) -> bool:
    nstr = str(n)
    max_segment_len = int(len(nstr) / 2)
    for i in range(1, max_segment_len + 1):
        if len(nstr) % i == 0:
            if nstr == nstr[i:] + nstr[:i]:
                return True
    return False


def two(instr: str) -> int:
    parsed = parse(instr)
    n = 0
    for (start, end) in parsed:
        for i in range(start, end + 1):
            if has_repeated_segments(i):
                n += i
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
