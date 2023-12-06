import sys
import re
from typing import Optional
from dataclasses import dataclass


@dataclass
class Transition:
    dest_start: int
    src_start: int
    n: int

    def __init__(self, dest_start: int, src_start: int, n: int):
        self.dest_start = dest_start
        self.src_start = src_start
        self.n = n
    
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


def one(instr: str) -> int:
    seeds, state_transitions, transition_functions = parse(instr)

    min_location: Optional[int] = None

    for item_id in seeds:
        item_type = "seed"
        while item_type != "location":
            for transition in transition_functions[item_type]:
                if transition.is_applicable_to(item_id):
                    item_id = transition.get_next_value(item_id)
                    break
            item_type = state_transitions[item_type]
        
        if min_location is None or item_id < min_location:
            min_location = item_id

    return min_location


def two(instr: str):
    seeds, state_transitions, transition_functions = parse(instr)
    assert len(seeds) % 2 == 0

    # seed_ranges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

    # inverted_states = list(reversed(state_transitions.keys()))

    # candidates = []

    # for level in inverted_states:
    #     for transition in transition_functions[level]:
    #         candidates += [transition.dest_start, transition.dest_start-1, transition.get_dest_end(), transition.get_dest_end() + 1]
        
    #     for i, ev in enumerate(candidates):
    #         for transition in transition_functions[level]:
    #             if transition.is_inverse_applicable_to(ev):
    #                 candidates[i] = transition.get_previous_value(ev)

    # candidates = list(filter(lambda x: x > 0, set(candidates))) # deduplicate and filter weird values

    # _debug(candidates)

    # trimmed_candidates = []

    # for x in candidates:
    #     matches_all = False

    #     for transition in transition_functions["seed"]:
    #         _debug(transition)
    #         if transition.dest_start <= x <= transition.get_dest_end():
    #             matches_all = True
    #             break

    #     if matches_all:
    #         trimmed_candidates.append(x)

    # _debug(trimmed_candidates)

    # ---

    # # Work out min-max seed numbers
    # min_seed_id = min(x for x in seeds[::2])
    # max_seed_id = max((seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2))

    # vals = []

    # for (lower_seed_id, n) in seed_ranges:
    #     endpoints = [lower_seed_id, lower_seed_id + n - 1]
        
    #     level = "seed"
    #     while level != "location":
    #         _debug(level, list(sorted(endpoints)))

    #         transitions = transition_functions[level]

    #         min_endp, max_endp = min(endpoints), max(endpoints)

    #         for transition in transitions:
                
    #             if min_endp < transition.src_start < max_endp:
    #                 endpoints.append(transition.src_start)

    #             if min_endp < (se := transition.get_src_end()) < max_endp:
    #                 endpoints.append(se)

    #         for i, ev in enumerate(endpoints):
    #             for transition in transitions:
    #                 if transition.is_applicable_to(ev):
    #                     endpoints[i] = transition.get_next_value(ev)
    #                     break

    #         level = state_transitions[level]

    #     _debug()

    #     vals = vals + endpoints

    # # _debug(list(sorted(vals)))

    # return min(filter(lambda x: x != 0, vals))


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