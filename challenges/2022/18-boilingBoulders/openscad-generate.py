import sys

inp = sys.stdin.read()

print(len(inp), file=sys.stderr)

print("union(){")

for line in inp.strip().splitlines():
    print(f"\ttranslate([{line}]) cube(1);")

print("};")
