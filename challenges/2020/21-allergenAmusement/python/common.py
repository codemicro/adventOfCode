from typing import List, Set, Tuple, Dict
import re


class Food:
    ingredients: List[str]
    known_allergens: Set[str]

    def __init__(self, ingredients: List[str], known_allergens: Set[str]) -> None:
        self.ingredients = ingredients
        self.known_allergens = known_allergens


def parse(instr: str) -> Tuple[List[Food], Set[str]]:

    foods = []
    all_allergens = set()

    for x in instr.strip().split("\n"):

        m = re.match(r"(.+) \(contains (.+)\)", x)
        if m is None:
            raise ValueError("input string does not match required format")

        ingredients = m.group(1).split(" ")
        allergens = set(m.group(2).split(", "))
        all_allergens = all_allergens.union(allergens)

        foods.append(Food(ingredients, allergens))

    return foods, all_allergens


def get_possibilities(foods: List[Food], allergens: Set[str]) -> Dict[str, Set[str]]:
    possibilities = {n: set() for n in allergens}

    for food in foods:
        for known_allergen in food.known_allergens:
            if len(possibilities[known_allergen]) == 0:
                possibilities[known_allergen] = set(food.ingredients)
            else:
                possibilities[known_allergen] = (
                    set(food.ingredients) & possibilities[known_allergen]
                )

    return possibilities
