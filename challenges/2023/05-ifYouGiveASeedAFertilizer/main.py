import sys
import re
from typing import Optional
from dataclasses import dataclass
import math
from functools import reduce


@dataclass
class Transition:
    dest_start: int
    src_start: int
    n: int

    def __init__(self, dest_start: int, src_start: int, n: int):
        self.dest_start = dest_start
        self.src_start = src_start
        self.n = n
    
    def get_delta(self) -> int:
        return self.dest_start - self.src_start

    def get_src_end(self) -> int:
        return self.src_start + self.n - 1

    def get_dest_end(self) -> int:
        return self.dest_start + self.n - 1

    def is_applicable_to(self, x: int) -> bool:
        return self.src_start <= x <= self.get_src_end()

    def is_inverse_applicable_to(self, x: int) -> bool:
        return self.dest_start <= x <= self.get_dest_end()

    def get_next_value(self, x: int) -> int:
        return (x - self.src_start) + self.dest_start

    def get_previous_value(self, x: int) -> int:
        return x + self.src_start - self.dest_start


def parse(instr: str) -> tuple[list[int], dict[str, str], dict[str, list[Transition]]]:
    state_transitions = {}
    transition_functions = {}
    seeds = []

    blocks = instr.split("\n\n")
    for block in blocks:
        if block.startswith("seeds: "):
            seeds = [int(x) for x in block.lstrip("seeds: ").strip().split(" ")]
        else:
            lines = block.splitlines()
            m = re.match(r"([a-z]+)-to-([a-z]+) map:", lines[0])
            assert m, f"invalid block: {lines[0]=}"

            from_type, to_type = m.groups()

            state_transitions[from_type] = to_type

            li = []
            for number_line in lines[1:]:
                sp = number_line.split(" ")
                assert len(sp) == 3
                li.append(Transition(*[int(x) for x in sp]))

            transition_functions[from_type] = li

    return seeds, state_transitions, transition_functions


def resolve(x: int, level: str, state_transitions, transition_functions) -> int:
    while level != "location":
        for transition in transition_functions[level]:
            if transition.is_applicable_to(x):
                x = transition.get_next_value(x)
                break
        level = state_transitions[level]

    return x


def apply_level(transition_functions: dict[str, list[Transition]], level: str, val: int) -> int:
    for transition in transition_functions[level]:
        if transition.is_applicable_to(val):
            return transition.get_next_value(val)
    return val


def apply_transitions(seeds: list[int], state_transitions: dict[str, str], transition_functions: dict[str, list[Transition]]) -> list[int]:
    res = []

    for item_id in seeds:
        item_type = "seed"
        while item_type != "location":
            item_id = apply_level(transition_functions, item_type, item_id)
            item_type = state_transitions[item_type]
        
        res.append(item_id)

    return res


def one(instr: str) -> int:
    return min(apply_transitions(*parse(instr)))


def two(instr: str):
    seeds, state_transitions, transition_functions = parse(instr)
    assert len(seeds) % 2 == 0

    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append((seeds[i], seeds[i]+seeds[i+1]-1))

    level = "seed"
    while level in transition_functions:
        _debug(level, ranges)
        neoranges = []

        while ranges:
            (range_start, range_end) = ranges.pop(0)

            modded = False
            for fn in transition_functions[level]:
                fn_start = fn.src_start
                fn_end = fn.get_src_end()
                delta = fn.get_delta()

                if range_start < fn_start and fn_start <= range_end <= fn_end:
                    ranges.append((fn_start, range_end))
                    neoranges.append((range_start + delta, fn_start - 1 + delta))
                    modded = True
                    break
                
                if fn_start <= range_start and range_end <= fn_end:
                    neoranges.append((range_start + delta, range_end + delta))
                    modded = True
                    break

                if fn_start <= range_start <= fn_end and fn_end < range_end:
                    neoranges.append((range_start + delta, fn_end + delta))
                    ranges.append((fn_end + 1, range_end))
                    modded = True
                    break

            if not modded:
                neoranges.append((range_start, range_end))

        ranges = neoranges
        level = state_transitions[level]

    _debug(ranges)

    return min(map(lambda x: x[0], ranges))


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
