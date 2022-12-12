from functools import reduce
from typing import *
from aocpy import BaseChallenge
from dataclasses import dataclass
import re


starting_items_regex = re.compile(r" *Starting items: ((?:\d+,? ?)+)")
operation_regex = re.compile(r" *Operation: new = (.+)")
test_regex = re.compile(r" *Test: divisible by (\d+)")
true_regex = re.compile(r" *If true: throw to monkey (\d+)?")
false_regex = re.compile(r" *If false: throw to monkey (\d+)?")


def compile_operation(expr: str) -> Callable[[int], int]:
    a, op, b = expr.split(" ")
    assert a == "old"
    assert op == "*" or op == "+"

    if op == "*":
        if b == "old":
            return lambda x: x * x
        else:
            bi = int(b)
            return lambda x: x * bi

    elif op == "+":
        if b == "old":
            return lambda x: x + x
        else:
            bi = int(b)
            return lambda x: x + bi

    assert False, "unreachable"


@dataclass
class Monkey:
    items: List[int]
    op: Callable[[int], int]
    divisor: int
    if_true: int
    if_false: int

    inspections: int

    def __init__(self, inp: str):   
        self.inspections = 0

        parts = inp.splitlines()[1:]
        self.items = list(map(int, starting_items_regex.match(parts[0]).group(1).split(", ")))
        self.divisor = int(test_regex.match(parts[2]).group(1))
        self.if_true = int(true_regex.match(parts[3]).group(1))
        self.if_false = int(false_regex.match(parts[4]).group(1))
        self.op = compile_operation(operation_regex.match(parts[1]).group(1))

    def inspect_first(self) -> int:
        self.inspections += 1

        item = self.items.pop(0)
        item = self.op(item)
        return item

    def calculate_throw(self, item: int) -> int:
        return self.if_true if item % self.divisor == 0 else self.if_false


def parse(instr: str) -> List[Monkey]:
    raw_monkies = instr.strip().split("\n\n")
    monke = []
    for rm in raw_monkies:
        monke.append(Monkey(rm))
    return monke


def run(inp: List[Monkey], n: int, mod: Callable[[int], int]) -> int:
    for _ in range(n):
        for monkey in inp:
            while len(monkey.items) != 0:
                item = monkey.inspect_first()
                item = mod(item)
                next_monkey = monkey.calculate_throw(item)
                
                inp[next_monkey].items.append(item)

    a, b = list(sorted(inp, reverse=True, key=lambda x: x.inspections))[:2]
    return a.inspections * b.inspections


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        return run(inp, 20, lambda x: x // 3)
        
    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)
        p = reduce(lambda x, y: x * y, map(lambda x: x.divisor, inp))
        return run(inp, 10000, lambda x: x % p)
