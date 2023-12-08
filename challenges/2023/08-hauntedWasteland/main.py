import sys
import re
from functools import reduce
import math


def parse(instr: str) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions, raw_graph = instr.split("\n\n")
    graph = {}

    for (this_node, left, right) in re.findall(
        r"([A-Z\d]{3}) = \(([A-Z\d]{3}), ([A-Z\d]{3})\)", raw_graph
    ):
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


def two(instr: str):
    instructions, graph = parse(instr)

    cursors = []
    for key in graph:
        if key[-1] == "A":
            cursors.append(key)

    loop_lengths = []

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

        assert reduce(
            lambda acc, v: acc or v[0][-1] == "Z", history, False
        ), f"{start} has no end condition"

        loop_start_key = (cursor, instruction_step)
        loop_starts_at = history[loop_start_key]

        loop_lengths.append((max(history.values()) - loop_starts_at) + 1)

    return math.lcm(*loop_lengths)


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
