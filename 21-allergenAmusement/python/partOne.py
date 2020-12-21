from common import *


def partOne(instr: str) -> int:
    foods, allergens = parse(instr)
    possibilities = get_possibilities(foods, allergens)

    bad_ingredients = set()
    for x in possibilities:
        bad_ingredients.update(possibilities[x])

    count = 0
    for food in foods:
        for ingredient in food.ingredients:
            if ingredient not in bad_ingredients:
                count += 1

    return count
