import sys
import functools


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


def get_max_joltage(n: int, bank: tuple[int]) -> int:
    assert len(bank) >= n

    if n == 0:
        return 0

    if n != 1:
        test_bank = bank[: -(n - 1)]
    else:
        test_bank = bank

    highest, idx = get_highest(test_bank)
    return highest * (10 ** (n - 1)) + get_max_joltage(n - 1, bank[idx + 1 :])


def one(instr: str) -> int:
    return sum(map(functools.partial(get_max_joltage, 2), parse(instr)))


def two(instr: str) -> int:
    return sum(map(functools.partial(get_max_joltage, 12), parse(instr)))


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
