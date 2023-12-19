import sys
from collections import namedtuple
from functools import reduce


ConditionalRule = namedtuple("ConditionalRule", ["field", "op", "value", "next"])
UnconditionalRule = namedtuple("UnconditionalRule", ["next"])
Rule = ConditionalRule | UnconditionalRule
Workflows = dict[str, list[Rule]]

Part = namedtuple("Part", ["x", "m", "a", "s"])


def parse(instr: str) -> tuple[Workflows, list[Part]]:
    raw_workflows, raw_parts = instr.split("\n\n")

    workflows: Workflows = {}

    for line in raw_workflows.splitlines():
        bracket_start = line.find("{")
        workflow_name = line[0:bracket_start]
        rules = []

        for raw_rule in line[bracket_start + 1 : -1].split(","):
            colon_pos = raw_rule.find(":")

            if colon_pos == -1:
                rules.append(UnconditionalRule(raw_rule))
                continue

            field = raw_rule[0]
            op = raw_rule[1]
            value = int(raw_rule[2:colon_pos])
            next_workflow = raw_rule[colon_pos + 1 :]

            rules.append(ConditionalRule(field, op, value, next_workflow))

        workflows[workflow_name] = rules

    parts: list[Part] = []
    for line in raw_parts.splitlines():
        line = line[1:-1]
        sp = [x.split("=") for x in line.split(",")]
        assert "".join(map(lambda x: x[0], sp)) == "xmas"
        parts.append(Part(*map(lambda x: int(x[1]), sp)))

    return workflows, parts


def test_rule(r: ConditionalRule, p: Part) -> bool:
    test_value = p.__getattribute__(r.field)
    match r.op:
        case ">":
            return test_value > r.value
        case "<":
            return test_value < r.value
        case _:
            raise ValueError(f"unknown operation {r.op}")


def is_acceptable(w: Workflows, p: Part) -> bool:
    cursor = "in"
    while not (cursor == "R" or cursor == "A"):
        for rule in w[cursor]:
            if (type(rule) == ConditionalRule and test_rule(rule, p)) or type(
                rule
            ) == UnconditionalRule:
                cursor = rule.next
                break
    return cursor == "A"


def one(instr: str):
    workflows, parts = parse(instr)

    acc = 0
    for part in parts:
        if is_acceptable(workflows, part):
            acc += sum(part)
    return acc


Range = tuple[int, int]


def split_range(rng: Range, rule: ConditionalRule) -> tuple[Range | None, Range | None]:
    # First range is the matching one, second range is the non-matching one.
    (lower, upper) = rng
    match rule.op:
        case "<":
            if upper < rule.value:
                return rng, None
            if lower >= rule.value:
                return None, rng
            return ((lower, rule.value - 1), (rule.value, upper))
        case ">":
            if lower > rule.value:
                return rng, None
            if upper <= rule.value:
                return None, rng
            return ((rule.value + 1, upper), (lower, rule.value))
        case _:
            raise ValueError(f"unknown operation {rule.op}")


def get_acceptable_ranges(
    workflows: Workflows, workflow_name: str, ranges: dict[str, Range]
) -> list[dict[str, Range]]:
    if workflow_name == "A":
        return [ranges]
    if workflow_name == "R":
        return []

    res = []

    for rule in workflows[workflow_name]:
        if type(rule) == UnconditionalRule:
            res += get_acceptable_ranges(workflows, rule.next, ranges)
            continue

        matches, not_matches = split_range(ranges[rule.field], rule)

        if matches is not None:
            x = ranges.copy()
            x[rule.field] = matches
            res += get_acceptable_ranges(workflows, rule.next, x)

        if not_matches is not None:
            ranges[rule.field] = not_matches

    return res


def get_range_len(r: Range) -> int:
    (start, end) = r
    return (end - start) + 1


def two(instr: str):
    workflows, _ = parse(instr)
    acc = 0
    for ranges in get_acceptable_ranges(
        workflows, "in", {c: [1, 4000] for c in "xmas"}
    ):
        acc += reduce(lambda acc, x: acc * get_range_len(x), ranges.values(), 1)
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
