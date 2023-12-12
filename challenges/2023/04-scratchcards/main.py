import sys
from dataclasses import dataclass
import functools
from typing import Callable


@dataclass()
class Card:
    id: int
    winning: set[int]
    present: set[int]

    def __init__(self, id: int):
        self.id = id
        self.winning = set()
        self.present = set()

    def __hash__(self) -> int:
        return hash(self.id)

    def get_winning_numbers(self) -> set[int]:
        return self.winning & self.present

    def calculate_score(self) -> int:
        n = len(self.get_winning_numbers())
        score = 0 if n == 0 else 2 ** (n - 1)
        return score

    def get_prize_copies(self) -> set[int]:
        return set(
            map(lambda x: self.id + x + 1, range(len(self.get_winning_numbers())))
        )


def make_card_counter(all_cards: list[Card]) -> Callable[[Card], int]:
    @functools.cache
    def fn(c: Card) -> int:
        acc = 1
        won = c.get_prize_copies()

        for won_card in won:
            acc += fn(all_cards[won_card - 1])

        return acc

    return fn


def parse(instr: str) -> list[Card]:
    res = []

    for line in instr.splitlines():
        card_decl, numbers_sect = line.split(": ")

        card = Card(int(card_decl.lstrip("Card ")))

        winning, present = numbers_sect.split("|")
        card.winning = set([int(x) for x in winning.split(" ") if x != ""])
        card.present = set([int(x) for x in present.split(" ") if x != ""])

        res.append(card)

    return res


def one(instr: str) -> int:
    cards = parse(instr)
    return sum(x.calculate_score() for x in cards)


def two(instr: str) -> int:
    cards = parse(instr)
    acc = 0

    count_fn = make_card_counter(cards)

    for card in cards:
        acc += count_fn(card)
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
