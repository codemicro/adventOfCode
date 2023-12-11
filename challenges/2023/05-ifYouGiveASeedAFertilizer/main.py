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

    inverted_transitions = {(k := tuple(reversed(x)))[0]: k[1] for x in state_transitions.items()}

    end_stop = max(seeds[i-1]+seeds[i] for i in range(1, len(seeds), 2))

    for i in range(0, end_stop):
        c = i
        level = "location"
        while level != "seed":
            level = inverted_transitions[level]
            for fn in transition_functions[level]:
                if fn.is_inverse_applicable_to(c):
                    c = fn.get_previous_value(c)
                    break

        for x in range(0, len(seeds), 2):
            start = seeds[x]
            end = seeds[x+1] + start - 1

            if start <= c <= end:
                return i

        i += 1

    return -1


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
