import sys
from collections import defaultdict


def parse(instr: str) -> tuple[list[int], list[int]]:
    a, b = [], []
    
    for line in instr.splitlines():
        ai, bi = line.split("   ")
        a.append(int(ai))
        b.append(int(bi))
        
    return a, b


def one(instr: str) -> int:
    a, b = parse(instr)
    
    a = sorted(a)
    b = sorted(b)
    
    acc = 0
    for (x, y) in zip(a, b):
        acc += abs(y - x)
        
    return acc


def two(instr: str):
    a, b = parse(instr)
    
    counts = defaultdict(lambda: 0)
    for val in b:
        counts[val] = counts[val] + 1
    
    acc = 0
    for val in a:
        acc += counts[val] * val
    
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