import sys
from typing import Optional


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def parse(inp: str) -> list[str]:
    return inp.splitlines()


def one(inp: str) -> int:
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


def find_first(inp: str, opts: list[str]) -> Optional[str]:
    candidates = []
    for opt in opts:
        if (p := inp.find(opt)) != -1:
            candidates.append((p, opt))
    li = sorted(candidates, key=lambda x: x[0])
    if len(li) == 0:
        return None
    return li[0][1]


def two(inp: str) -> int:
    parsed = parse(inp)
    acc = 0

    search_values = list(map(str, range(0, 10))) + list(TRANSFORMATIONS.keys())
    reversed_search_values = ["".join(reversed(x)) for x in search_values]

    for line in parsed:
        first_digit = find_first(line, search_values)
        second_digit = find_first("".join(reversed(line)), reversed_search_values)
        assert (
            first_digit is not None and second_digit is not None
        ), f"must have at least one digit per line: {line}"

        # second digit will be the reversed form
        second_digit = "".join(reversed(second_digit))

        first_digit = TRANSFORMATIONS.get(first_digit, first_digit)
        second_digit = TRANSFORMATIONS.get(second_digit, second_digit)

        val = first_digit + second_digit
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
