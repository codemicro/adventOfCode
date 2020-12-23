from common import *


def partOne(instr: str) -> int:
    cups = parse(instr)

    total_cups = len(cups)

    current_cup = 0
    current_cup_val = cups[0]
    for i in range(100):

        print(i + 1, cups)

        # pick up next three cups
        next_three = []
        print("  ", end="")
        for i in range(3):
            ni = current_cup + 1 + i
            if ni >= len(cups):
                ni -= len(cups)
            print(ni, cups[ni], end=", ")
            next_three.append(cups[ni])
        print()
        print("  next three ", next_three)

        for rm in next_three:
            cups.remove(rm)

        # select destination cup
        destination_cup_val = current_cup_val - 1
        while destination_cup_val in next_three or destination_cup_val not in cups:

            print("  before dv", destination_cup_val)

            destination_cup_val -= 1
            if destination_cup_val <= min(cups + next_three):
                destination_cup_val += 1 + max(cups + next_three)
                print("  looping dv to", destination_cup_val)

            print("  after dv", destination_cup_val, max(cups + next_three))
        destination_cup = cups.index(destination_cup_val)

        print("  destination", destination_cup_val)

        # insert cups immediately clockwise of destination
        for v in next_three[::-1]:
            cups.insert(destination_cup + 1, v)

        # rotate the list so the current cup is in the same place it started at
        while current_cup_val != cups[current_cup]:
            t = cups.pop(0)
            cups.append(t)

        # select new current cup
        current_cup += 1
        if current_cup >= total_cups:
            current_cup -= total_cups
        current_cup_val = cups[current_cup]

        print()


    # rotate until 1 is the first value
    while cups[0] != 1:
        t = cups.pop(0)
        cups.append(t)

    print(cups)

    return int("".join([str(x) for x in cups[1:]]))
