import sys
from typing import Optional


def parse(instr: str) -> list[list[int]]:
    res = []
    for line in instr.splitlines():
        res.append(list(map(int, line.split(" "))))
    return res


def test_pair(
    a: int, b: int, sequence_is_negative: Optional[bool]
) -> tuple[bool, bool]:
    diff = b - a
    this_is_negative = diff < 0

    if sequence_is_negative is not None and this_is_negative != sequence_is_negative:
        return False, this_is_negative

    return 1 <= abs(diff) <= 3, this_is_negative


def test_report(rep: list[int]) -> bool:
    should_be_negative: Optional[bool] = None
    ok = False

    for i, v in enumerate(rep[:-1]):
        w = rep[i + 1]

        ok, neg = test_pair(v, w, should_be_negative)
        if should_be_negative is None:
            should_be_negative = neg

        if not ok:
            break

    return ok


def one(instr: str):
    reports = parse(instr)

    n = 0
    for rep in reports:
        if test_report(rep):
            n += 1

    return n


def two(instr: str):
    reports = parse(instr)

    n = 0
    for rep in reports:
        if test_report(rep):
            n += 1
        else:
            ok = False
            for i in range(len(rep)):
                r = rep.copy()
                r.pop(i)
                if test_report(r):
                    ok = True
                    break

            if ok:
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
