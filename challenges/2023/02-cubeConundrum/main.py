import sys
from dataclasses import dataclass


@dataclass(init=False)
class Game:
    id: int
    hands: list[dict[str, int]]

    def __init__(self, id: int):
        self.id = id
        self.hands = []


def parse(inp: str) -> list[Game]:
    res = []
    for line in inp.splitlines():
        game_decl, game_hands = line.split(": ")

        game = Game(int(game_decl.lstrip("Game ")))

        for hand in game_hands.split(";"):
            hand = hand.strip()
            counts = {}
            for part in hand.split(", "):
                n, colour = part.split(" ")
                counts[colour] = int(n)
            game.hands.append(counts)

        res.append(game)

    return res


COLOUR_MAXVALS = {"red": 12, "green": 13, "blue": 14}


def one(inp: str):
    games = parse(inp)

    acc = 0

    for game in games:
        ok = True

        for hand in game.hands:
            for key in COLOUR_MAXVALS:
                if COLOUR_MAXVALS[key] < hand.get(key, 0):
                    ok = False
                    break

            if not ok:
                break

        if ok:
            acc += game.id

    return acc


def two(inp: str):
    games = parse(inp)
    acc = 0

    for game in games:
        x = 1

        for colour in COLOUR_MAXVALS.keys():
            x *= max(map(lambda x: x.get(colour, 0), game.hands))

        acc += x

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
