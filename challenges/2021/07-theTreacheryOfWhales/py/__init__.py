from typing import List
from aocpy import BaseChallenge
import math


def parse(instr: str) -> List[int]:
    return list(map(int, instr.strip().split(",")))


def increasing_fuel_sum_to_position(crabs: List[int], position: int) -> int:
    sigma = 0
    for crab in crabs:
        dist = abs(position - crab)
        sigma += sum(i + 1 for i in range(dist))
    return sigma


def linear_fuel_sum_to_position(crabs: List[int], position: int) -> int:
    sigma = 0
    for crab in crabs:
        sigma += abs(position - crab)
    return sigma


def median_distance(crabs: List[int]) -> int:
    crabs = list(sorted(crabs))
    num_crabs = len(crabs)
    n = None
    if num_crabs % 2 == 0:  # is even, therefore interpolate :(
        high = crabs[int(num_crabs / 2)]
        low = crabs[int(num_crabs / 2) - 1]
        delta = high - low
        n = low + int(delta / 2)
    else:  # odd, take raw middle value
        n = crabs[math.floor(num_crabs / 2)]
    return n


def mean_distance(crabs: List[int]) -> float:
    return sum(crabs) / len(crabs)


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        crab_distances = parse(instr)
        n = median_distance(crab_distances)
        return linear_fuel_sum_to_position(crab_distances, n)

    @staticmethod
    def two(instr: str) -> int:
        crabs = parse(instr)
        n = mean_distance(crabs)

        low = increasing_fuel_sum_to_position(crabs, math.floor(n))
        high = increasing_fuel_sum_to_position(crabs, math.ceil(n))

        return min(low, high)
