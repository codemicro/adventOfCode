import sys
from enum import IntEnum
import functools
from typing import Callable, Optional


def parse(instr: str) -> list[tuple[str, int]]:
    return [((sp := x.split(" "))[0], int(sp[1])) for x in instr.splitlines()]


def count_chars(x: str) -> dict[str, int]:
    res = {}
    for ch in x:
        res[ch] = res.get(ch, 0) + 1
    return res


class HandType(IntEnum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


def get_hand_type(hand: str, counts: Optional[dict[str, int]] = None) -> HandType:
    if counts is None:
        counts = count_chars(hand)
    num_unique_chars = len(counts)

    if num_unique_chars == 5:
        return HandType.HighCard

    if num_unique_chars == 4:
        return HandType.OnePair

    if num_unique_chars == 1:
        return HandType.FiveOfAKind

    sorted_counts = list(sorted(counts.values()))

    if num_unique_chars == 3:
        if sorted_counts == [1, 2, 2]:
            return HandType.TwoPair
        return HandType.ThreeOfAKind

    if num_unique_chars == 2:
        if sorted_counts == [1, 4]:
            return HandType.FourOfAKind
        return HandType.FullHouse

    raise ValueError(f"bad hand {hand}")


def get_best_hand_type(hand: str) -> HandType:
    counts = count_chars(hand)

    if "J" in counts:
        num_jokers = counts["J"]

        if num_jokers == 5:
            return HandType.FiveOfAKind

        del counts["J"]
        most_frequent_card = max(counts, key=lambda x: counts[x])
        counts[most_frequent_card] = counts[most_frequent_card] + num_jokers

    return get_hand_type(hand, counts=counts)


def compare_card(a: str, b: str, ranking_sequence: list[str]) -> int:
    ca, cb = ranking_sequence.index(a), ranking_sequence.index(b)

    if ca > cb:
        return 1

    if ca < cb:
        return -1

    return 0


def compare_hands(
    a: str, b: str, ranking_sequence: list[str], hand_type: Callable[[str], HandType]
) -> int:
    hta, htb = hand_type(a), hand_type(b)

    if hta > htb:
        return 1

    if hta < htb:
        return -1

    for (ca, cb) in zip(a, b):
        if ca != cb:
            return compare_card(ca, cb, ranking_sequence)

    return 0


def run(
    instr: str, sequence: list[str], hand_type_fn: Callable[[str], HandType]
) -> int:
    @functools.cmp_to_key
    def cmp_fn(a: tuple[str, any], b: tuple[str, any]) -> int:
        return compare_hands(a[0], b[0], sequence, hand_type_fn)

    plays = parse(instr)
    acc = 0
    for i, (_, bid) in enumerate(sorted(plays, key=cmp_fn)):
        acc += bid * (i + 1)
    return acc


def one(instr: str):
    return run(
        instr,
        ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"],
        get_hand_type,
    )


def two(instr: str):
    return run(
        instr,
        ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"],
        get_best_hand_type,
    )


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
