import sys
from collections import namedtuple, defaultdict
import math


OrderingRule = namedtuple("OrderingRule", ["page", "goes_before"])


def parse(instr: str) -> tuple[list[OrderingRule], list[list[int]]]:
    rules, sets = instr.split("\n\n")

    return (
        [OrderingRule(*map(int, line.split("|"))) for line in rules.splitlines()],
        [list(map(int, line.split(","))) for line in sets.splitlines()],
    )


def generate_rule_map(rules: list[OrderingRule]) -> dict[int, list[int]]:
    rule_map = defaultdict(lambda: [])
    for rule in rules:
        rule_map[rule.page].append(rule.goes_before)
    return rule_map


def is_pageset_valid(rule_map: dict[int, list[int]], pageset: list[int]) -> bool:
    for i, v in enumerate(pageset):
        before = pageset[:i]

        for following_number in rule_map[v]:
            if following_number in before:
                return False
    return True


def get_middle_number(x: list[int]) -> int:
    assert len(x) % 2 == 1, f"{x} has no nice middle point"
    return x[int((len(x) - 1) / 2)]


def one(instr: str):
    rules, pagesets = parse(instr)
    rule_map = generate_rule_map(rules)  # for each item, these items should be after it

    acc = 0
    for pageset in pagesets:
        if is_pageset_valid(rule_map, pageset):
            acc += get_middle_number(pageset)

    return acc


def two(instr: str):
    rules, pagesets = parse(instr)
    rule_map = generate_rule_map(rules)

    inverse_rule_map = defaultdict(
        lambda: []
    )  # for each item, these items should be before it
    for rule in rules:
        inverse_rule_map[rule.goes_before].append(rule.page)

    acc = 0
    for pageset in filter(lambda x: not is_pageset_valid(rule_map, x), pagesets):
        while not is_pageset_valid(rule_map, pageset):
            for i in range(len(pageset)):
                for j in range(i + 1, len(pageset)):
                    iv = pageset[i]
                    jv = pageset[j]

                    if jv in inverse_rule_map[iv] and i < j:
                        pageset[i], pageset[j] = pageset[j], pageset[i]

        acc += get_middle_number(pageset)

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
