from common import *
import time

def play_round(deck_one: List[int], deck_two: List[int]) -> None:

    top_one = deck_one.pop(0)
    top_two = deck_two.pop(0)

    if top_one > top_two:
        deck_one.append(top_one)
        deck_one.append(top_two)
    elif top_two > top_one:
        deck_two.append(top_two)
        deck_two.append(top_one)


def partOne(instr: str) -> int:
    deck_one, deck_two = parse(instr)

    while len(deck_one) > 0 and len(deck_two) > 0:
        play_round(deck_one, deck_two)

    return calc_score(deck_one if len(deck_one) != 0 else deck_two)
