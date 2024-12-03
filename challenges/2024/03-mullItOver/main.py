import sys
import re


Instruction = tuple[str, int, int]


def parse(instr: str) -> list[Instruction]:
    r = re.compile(r"(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)")
    res = []
    for m in r.findall(instr):
        if m[0]:
            res.append(("mul", int(m[1]), int(m[2])))
        elif m[3]:
            res.append(("do", 0, 0))
        elif m[4]:
            res.append(("don't", 0, 0))
    return res


def one(instr: str):
    instructions = parse(instr)

    acc = 0
    for (op, a, b) in instructions:
        if op == "mul":
            acc += a * b

    return acc


def two(instr: str):
    instructions = parse(instr)

    acc = 0
    on = True
    for (op, a, b) in instructions:
        if op == "mul" and on:
            acc += a * b
        elif op == "do":
            on = True
        elif op == "don't":
            on = False

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
