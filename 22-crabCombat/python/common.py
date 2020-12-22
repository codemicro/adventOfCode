from typing import List, Tuple


def parse(instr: str) -> Tuple[List[int], List[int]]:

    deck_one_str, deck_two_str = instr.strip().split("\n\n")

    deck_one = [int(x) for x in deck_one_str.split("\n")[1:]]
    deck_two = [int(x) for x in deck_two_str.split("\n")[1:]]

    return deck_one, deck_two


def calc_score(deck: List[int]) -> int:
    score = 0

    deck_len = len(deck)
    for i, v in enumerate(deck):
        score += v * (deck_len - i)

    return score
