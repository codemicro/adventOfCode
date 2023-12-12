import sys
from typing import Generator, Iterable


Rule = tuple[str, list[int]]


def parse(instr: str) -> list[Rule]:
    res = []
    for line in instr.splitlines():
        observations, lengths = line.split(" ")
        res.append((observations, tuple(map(int, lengths.split(",")))))
    return res


def generate_permutations(n: int) -> Generator[list[int], None, None]:
    if n == 0:
        yield []
        return
    for p in generate_permutations(n-1):
        for c in ".#":
            yield p + [c]
    

def generate_possible_observations(x: str) -> Generator[list[str], None, None]:
    xl = list(x)
    replacement_locations = [i for i in range(len(xl)) if xl[i] == "?"]
    for combs in generate_permutations((nrl := len(replacement_locations))):
        for i in range(nrl):
            xl[replacement_locations[i]] = combs[i]

        yield xl


def check_broken_length_constraints(x: Iterable[str], counts: list[int]) -> bool:
    inside_set = False
    set_length = 0
    current_count = 0
    for i in range((lx := len(x))+1):
        char = x[i] if i < lx else "-"
        if char == "#":
            inside_set = True
            set_length += 1
        elif inside_set:
            inside_set = False
            try:
                if set_length != counts[current_count]:
                    return False
            except IndexError:
                # too many counts exist
                return False
            set_length = 0
            current_count += 1
    return current_count == len(counts)


def one(instr: str):
    rules = parse(instr)

    acc = 0
    for (template, lengths) in rules:
        for obs in generate_possible_observations(template):
            if check_broken_length_constraints(obs, lengths):
                acc += 1
    return acc


def two(instr: str):
    return


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