from __future__ import annotations
from typing import *
from aocpy import BaseChallenge
from enum import Enum
import re


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    DIV = "/"
    MULT = "*"

    def inverse(self) -> Operator:
        if self.value == self.ADD.value:
            return self.SUB
        elif self.value == self.SUB.value:
            return self.ADD
        elif self.value == self.MULT.value:
            return self.DIV
        else:
            return self.MULT

    def calc(self, a_val, b_val) -> float:
        res = 0
        if self.value == self.ADD.value:
            res = a_val + b_val
        elif self.value == self.SUB.value:
            res = a_val - b_val
        elif self.value == self.MULT.value:
            res = a_val * b_val
        elif self.value == self.DIV.value:
            res = a_val / b_val

        return res


Monkey = Union[int, Tuple[str, Operator, str]]
Monkies = Dict[str, Monkey]


number_re = re.compile(r"([a-z]{4}): (\d+)")
operation_re = re.compile(r"([a-z]{4}): ([a-z]{4}) ([+\-/*]) ([a-z]{4})")


def parse(instr: str) -> Monkies:
    res: Dict[str, Monkey] = {}
    for line in instr.strip().splitlines():
        if x := number_re.match(line):
            name, num_str = x.groups()
            num = int(num_str)
            res[name] = num
        elif x := operation_re.match(line):
            name, a, op_str, b = x.groups()
            res[name] = (a, Operator(op_str), b)
    return res


def evaluate_monkey(monkey: Monkey, monkies: Monkies) -> float:
    if type(monkey) == int:
        return monkey

    elif type(monkey) == tuple:
        (a_name, op, b_name) = monkey
        a_val = evaluate_monkey(monkies[a_name], monkies)
        b_val = evaluate_monkey(monkies[b_name], monkies)
        return op.calc(a_val, b_val)

    raise ValueError(f"impossible type {type(monkey)}")


def does_branch_contain(target: str, monkey: Monkey, monkies: Monkies) -> bool:
    if type(monkey) == int:
        return False

    elif type(monkey) == tuple:
        (a_name, _, b_name) = monkey
        if a_name == target or b_name == target:
            return True

        if does_branch_contain(target, monkies[a_name], monkies):
            return True
        return does_branch_contain(target, monkies[b_name], monkies)

    raise ValueError(f"impossible type {type(monkey)}")


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        return int(evaluate_monkey(inp["root"], inp))

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)

        root = inp["root"]
        assert type(root) == tuple

        (a_name, _, b_name) = root

        if does_branch_contain("humn", inp[a_name], inp):
            branch_with_human = inp[a_name]
            target_value = evaluate_monkey(inp[b_name], inp)
        elif does_branch_contain("humn", inp[b_name], inp):
            branch_with_human = inp[b_name]
            target_value = evaluate_monkey(inp[a_name], inp)
        else:
            raise ValueError("neither root branch contains humn")

        acc = target_value
        cursor = branch_with_human
        while True:
            (a_name, op, b_name) = cursor

            if a_name == "humn" or does_branch_contain("humn", inp[a_name], inp):
                x = evaluate_monkey(inp[b_name], inp)
                is_first_arg = False
                cursor = inp[a_name]
            elif b_name == "humn" or does_branch_contain("humn", inp[b_name], inp):
                x = evaluate_monkey(inp[a_name], inp)
                is_first_arg = True
                cursor = inp[b_name]
            else:
                raise ValueError("neither branch contains humn")

            if op == Operator.ADD or op == Operator.MULT:
                acc = op.inverse().calc(acc, x)
            elif op == Operator.SUB:
                if is_first_arg:
                    acc = op.calc(-acc, -x)
                else:
                    acc = op.inverse().calc(acc, x)
            elif op == Operator.DIV:
                if is_first_arg:
                    acc = op.calc(1 / acc, 1 / x)
                else:
                    acc = op.inverse().calc(acc, x)
            else:
                raise ValueError(f"invalid operator {op}")

            if a_name == "humn" or b_name == "humn":
                break

        return int(acc)
