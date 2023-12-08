import sys
import re
from functools import reduce


def parse(instr: str) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions, raw_graph = instr.split("\n\n")
    graph = {}

    for (this_node, left, right) in re.findall(r"([A-Z\d]{3}) = \(([A-Z\d]{3}), ([A-Z\d]{3})\)", raw_graph):
         graph[this_node] = (left, right)

    return instructions, graph


def one(instr: str):
    instructions, graph = parse(instr)

    cursor = "AAA"
    i = 0
    while cursor != "ZZZ":
        instruction = instructions[i % len(instructions)]
        cursor = graph[cursor][0 if instruction == "L" else 1]
        i += 1

    return i


def are_cursors_at_z(cursors: list[str]) -> bool:
    for c in cursors:
        if c[-1] != "Z":
            return False
    return True


def two(instr: str):
    instructions, graph = parse(instr)

    cursors = []
    for key in graph:
        if key[-1] == "A":
            cursors.append(key)

    constraints = []

    for start in cursors:
        cursor = start
        instruction_step = 0
        
        history = {}
        i = 0

        while (cursor, instruction_step) not in history:
            instruction = instructions[instruction_step]
            history[(cursor, instruction_step)] = i
            cursor = graph[cursor][0 if instruction == "L" else 1]
            i += 1
            instruction_step = i % len(instructions)
        
        assert reduce(lambda acc, v: acc or v[0][-1] == "Z", history, False), f"{start} has no end condition"

        loop_start_key = (cursor, instruction_step)

        endpoint_at = None
        for key in history:
            if key[0][-1] == "Z":
                endpoint_at = history[key]
                _debug(key)

        loop_starts_at = history[loop_start_key]
        loop_length = (max(history.values()) - loop_starts_at) + 1

        _debug(f"{start} loops {loop_start_key} {loop_starts_at=} {endpoint_at=} {loop_length=}")

        constraints.append((loop_starts_at, endpoint_at - loop_starts_at, loop_length))

    m = 0
    soln = None

    while True:
        # _debug("---")

        if m % 1000 == 0:
            _debug(m, end="\r")

        works = True

        for (s, i, l) in constraints:
            x = (m-s-i)/l

            # _debug((s, i, l), x, (x < 0 or x % 1 != 0))

            if x < 0 or not float(x).is_integer():
                works = False
                break

        if works:
            soln = m
            break

        m += 1

    return soln


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