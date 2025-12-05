import sys
import itertools


def parse(instr: str) -> tuple[list[tuple[int, int]], list[int]]:
    ranges, ids = instr.split("\n\n")

    rres = []
    for line in ranges.splitlines():
        start, end = tuple(map(int, line.split("-")))
        rres.append((start, end))

    ires = list(map(int, ids.splitlines()))

    return rres, ires


def one(instr: str):
    ranges, ids = parse(instr)
    n = 0
    for ingredient_id in ids:
        for (start, end) in ranges:
            if start <= ingredient_id <= end:
                n += 1
                break
    return n


def two(instr: str):
    ranges, _ = parse(instr)

    START = 1
    END = -1

    sequence = list(
        sorted(
            itertools.chain(
                map(lambda x: (x[0], START), ranges),
                map(lambda x: (x[1], END), ranges),
            ),
            key=lambda x: x[0],
        )
    )

    count = 0
    i = 0
    while i < len(sequence):
        _, marker = sequence[i]

        if marker == START and count > 0:
            # we have a new start and we are already inside a block
            # delete this start and the next end we can find

            j = i + 1
            while j < len(sequence):
                _, marker = sequence[j]
                if marker == END:
                    break
                j += 1

            assert j != len(
                sequence
            ), "unbalanced sequence"  # this will be true when we get to the end of the list without `break`ing off, ie. without finding an end

            sequence.pop(j)
            sequence.pop(i)
        else:
            count += marker
            i += 1

    n = 0
    for (start, end) in zip(sequence[::2], sequence[1::2]):
        sn, sm = start
        en, em = end
        assert sm == START and em == END
        n += (en - sn) + 1
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
