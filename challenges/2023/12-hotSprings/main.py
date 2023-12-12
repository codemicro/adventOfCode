import sys
from typing import Iterable
from functools import cache, reduce


Rule = tuple[str, list[int]]


def parse(instr: str) -> list[Rule]:
    res = []
    for line in instr.splitlines():
        observations, lengths = line.split(" ")
        res.append((observations, tuple(map(int, lengths.split(",")))))
    return res


def unfold(rule: Rule) -> Rule:
    obs, lens = rule
    return ((obs + "?")*5)[:-1], lens * 5


@cache
def solve(observations: str, lengths: list[int]) -> int:
    if len(lengths) == 0:
        if "#" in observations:
            return 0
        return 1
    elif len(observations) == 0:
        return 0

    char = observations[0]
    if char == ".":
        return solve(observations[1:], lengths)

    if char == "?":
        a = solve("." + observations[1:], lengths)
        b = solve("#" + observations[1:], lengths)
        return a + b

    # assuming char == "#"

    target_len = lengths[0]
    if len(observations) < target_len:
        return 0

    if "." in observations[:target_len]:
        return 0


    if target_len + 1 <= len(observations):
        if observations[target_len] == "#":
            return 0
        if observations[target_len] == "?":
            return solve("." + observations[target_len+1:], lengths[1:])

    return solve(observations[target_len:], lengths[1:])


def run(rules: Iterable[Rule]) -> int:
    return reduce(lambda acc, x: acc + solve(*x), rules, 0)


def one(instr: str):
    return run(parse(instr))

def two(instr: str):
    return run(map(unfold, parse(instr)))


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