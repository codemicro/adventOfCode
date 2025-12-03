import sys


def parse(instr: str) -> list[tuple[int]]:
    return list(map(lambda x: tuple(map(int, x)), instr.splitlines()))


def get_highest(bank: tuple[int]) -> tuple[int, int]:
    max = -1
    max_i = 0
    for i, n in enumerate(bank):
        if n > max:
            max = n
            max_i = i
    return max, max_i


def get_max_joltage(bank: tuple[int], n: int) -> int:
    assert len(bank) >= n

    if n == 0:
        return 0

    if n != 1:
        test_bank = bank[: -(n - 1)]
    else:
        test_bank = bank

    highest, idx = get_highest(test_bank)
    return highest * (10 ** (n - 1)) + get_max_joltage(bank[idx + 1 :], n - 1)


def one(instr: str) -> int:
    banks = parse(instr)
    n = 0
    for bank in banks:
        mj = get_max_joltage(bank, 2)
        n += mj
    return n


def two(instr: str) -> int:
    banks = parse(instr)
    n = 0
    for bank in banks:
        mj = get_max_joltage(bank, 12)
        n += mj
    return n


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
