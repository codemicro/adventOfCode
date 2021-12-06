from typing import List, Dict
from aocpy import BaseChallenge


def parse(instr: str) -> List[int]:
    return list(map(int, instr.strip().split(",")))


def count_fish_by_timer(all_fish: List[int]) -> Dict[int, int]:
    m = {}
    for fish in all_fish:
        m[fish] = m.get(fish, 0) + 1
    return m


def iterate_fish_once(sum_dict: Dict[int, int]):
    nm = {}
    # shift back
    for i in range(9):
        nm[i - 1] = sum_dict.get(i, 0)
    # apply -1 value
    nm[6] = nm.get(6, 0) + nm.get(-1, 0)
    nm[8] = nm.get(-1, 0)
    del nm[-1]
    return nm


def sum_of_fish_after_n(fish: List[int], n: int) -> int:
    by_timer = count_fish_by_timer(fish)
    for _ in range(n):
        by_timer = iterate_fish_once(by_timer)
    return sum([by_timer[k] for k in by_timer])


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        fish = parse(instr)
        return sum_of_fish_after_n(fish, 80)

    @staticmethod
    def two(instr: str) -> int:
        fish = parse(instr)
        return sum_of_fish_after_n(fish, 256)
