import sys
from typing import Callable


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def parse(inp: str) -> list[str]:
    return inp.splitlines()


def one(inp: str):
    parsed = parse(inp)
    acc = 0
    for line in parsed:
        digits = list(filter(lambda x: x.isdigit(), line))
        assert len(digits) != 0, f"must have at least one digit per line: {line}"
        val = digits[0] + digits[-1]
        acc += int(val)
    return acc


TRANSFORMATIONS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def collect_all_digits(line: str) -> list[str]:
    res = []
    for i, char in enumerate(line):
        if char.isdigit():
            res.append(char)
            break
        outer_break = False
        for src in TRANSFORMATIONS:
            if line[i : min(len(line), i + len(src))] == src:
                res.append(TRANSFORMATIONS[src])
                outer_break = True
                break
            if outer_break:
                break

    rev_line = "".join(reversed(line))

    for i, char in enumerate(rev_line):
        if char.isdigit():
            res.append(char)
            break
        outer_break = False
        for src in TRANSFORMATIONS:
            if rev_line[i : min(len(line), i + len(src))] == "".join(reversed(src)):
                res.append(TRANSFORMATIONS[src])
                outer_break = True
                break
        if outer_break:
            break

    return res


def two(inp: str):
    parsed = parse(inp)
    acc = 0
    for line in parsed:
        digits = collect_all_digits(line)
        print(digits)
        assert len(digits) != 0, f"must have at least one digit per line: {line}"
        val = digits[0] + digits[-1]
        acc += int(val)
    return acc


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        sys.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))
