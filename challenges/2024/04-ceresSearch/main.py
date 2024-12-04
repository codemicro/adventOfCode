import sys
import gridutil.grid as grid
import gridutil.coord as coord


def parse(instr: str) -> grid.Grid:
    return grid.parse(instr.upper())


def one(instr: str):
    wordsearch = parse(instr)

    seq_starts = list(
        map(lambda x: x[0], filter(lambda x: x[1] == "X", wordsearch.items()))
    )
    detected_sequences = set()

    for start_pos in seq_starts:
        for xdir in [-1, 0, 1]:
            for ydir in [-1, 0, 1]:

                if xdir == 0 and ydir == 0:
                    continue

                delta = coord.Coordinate(xdir, ydir)

                ok = True
                for i, v in enumerate("XMAS"):
                    if not ok:
                        break

                    g = wordsearch.get(coord.add(start_pos, coord.mult(delta, i)), "-")
                    ok = g == v

                if ok:
                    detected_sequences.add((start_pos, delta))

    return len(detected_sequences)


def check_cross_adjacents(s: str) -> bool:
    return s == "SM" or s == "MS"


def two(instr: str):
    wordsearch = parse(instr)

    seq_starts = list(
        map(lambda x: x[0], filter(lambda x: x[1] == "A", wordsearch.items()))
    )
    detected_sequences = set()

    for start_pos in seq_starts:

        a = wordsearch.get(coord.add(start_pos, (-1, -1)), "") + wordsearch.get(
            coord.add(start_pos, (1, 1)), ""
        )
        b = wordsearch.get(coord.add(start_pos, (-1, 1)), "") + wordsearch.get(
            coord.add(start_pos, (1, -1)), ""
        )

        if check_cross_adjacents(a) and check_cross_adjacents(b):
            detected_sequences.add(start_pos)

    return len(detected_sequences)


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
