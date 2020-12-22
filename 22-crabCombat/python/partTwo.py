from common import *
import copy


def play_round(deck_one: List[int], deck_two: List[int]) -> Tuple[int, Tuple[List[int], List[int]]]:
    # returns winner number and decks in their new state

    # print("new round")

    seen_configurations = []

    while len(deck_one) > 0 and len(deck_two) > 0:
        if (deck_one, deck_two) in seen_configurations:
            # print("Seen this config before")
            return 1, (deck_one, deck_two)
        else:
            seen_configurations.append((copy.deepcopy(deck_one), copy.deepcopy(deck_two)))

        # do gameplay shenanigans
        top_one = deck_one.pop(0)
        top_two = deck_two.pop(0)

        winner = 0
        if len(deck_one) >= top_one and len(deck_two) >= top_two:
            # recurse! 🦀
            # print("recursing 🦀")

            new_deck_one = deck_one[:top_one]
            new_deck_two = deck_two[:top_two]

            winner, _ = play_round(new_deck_one, new_deck_two)
        else:
            # play as usual
            if top_one > top_two:
                winner = 1
            elif top_two > top_one:
                winner = 2

        # print(winner, "wins")

        # do things based on the winner    
        if winner == 1:
            deck_one.append(top_one)
            deck_one.append(top_two)
        elif winner == 2:
            deck_two.append(top_two)
            deck_two.append(top_one)
        else:
            raise Exception("SDFGKSHDFGKSHDFGAAAAAAAA!!!") # yes

    # print("finished this round")

    return 1 if len(deck_one) != 0 else 2, (deck_one, deck_two)


def partTwo(instr: str) -> int:
    deck_one, deck_two = parse(instr)

    winner, (deck_one, deck_two) = play_round(copy.deepcopy(deck_one), copy.deepcopy(deck_two))

    if winner == 1:
        return calc_score(deck_one)
    elif winner == 2:
        return calc_score(deck_two)

    return 0
