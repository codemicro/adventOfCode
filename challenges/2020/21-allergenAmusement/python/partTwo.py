from common import *


def partTwo(instr: str) -> None:
    foods, allergens = parse(instr)
    possibilities = get_possibilities(foods, allergens)

    definites = {}  # ingredients that definitely contain allergens

    # remove known things
    for possibility in possibilities:
        if len(possibilities[possibility]) == 1:
            definites[possibility] = possibilities[possibility].pop()

    for definite in definites:
        del possibilities[definite]

    while True:
        definite_set = set([definites[x] for x in definites])
        if len(possibilities) == 0:
            break

        to_del = []
        for possibility in possibilities:
            possibilities[possibility] = possibilities[possibility] - definite_set
            if len(possibilities[possibility]) == 0:
                to_del.append(possibility)
            elif len(possibilities[possibility]) == 1:
                definites[possibility] = possibilities[possibility].pop()

        for td in to_del:
            del possibilities[td]

    return ",".join(
        [
            x[1]
            for x in sorted([(x, definites[x]) for x in definites], key=lambda x: x[0])
        ]
    )
