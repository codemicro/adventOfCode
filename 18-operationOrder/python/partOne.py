from typing import List, Tuple, Union


def parse_expression(expression: str) -> Tuple[List, int]:
    o = []

    if len(expression) == 0:
        return o, 0

    ptr = 0
    while ptr < len(expression):
        char = expression[ptr]
        if char == "(":
            nl, idx = parse_expression(expression[ptr + 1 :])
            o.append(nl)
            ptr += idx
        elif char == ")":
            return o, ptr + 1
        else:
            o.append(char)

        ptr += 1

    return o, 0


def calc_to_int(x: Union[list, str]) -> int:
    if type(x) == list:
        return calculate(x)
    else:
        return int(x)


def calculate(expression: List) -> int:
    n = calc_to_int(expression[0])

    ptr = 1
    while ptr < len(expression):
        op = expression[ptr]
        x = calc_to_int(expression[ptr + 1])

        if op == "+":
            n += x
        elif op == "-":
            n -= x
        elif op == "*":
            n *= x
        elif op == "/":
            n /= x
        else:
            raise ValueError(f"unknown operator '{op}'")
        ptr += 2

    return n


def partOne(instr: str) -> int:
    expressions = [
        parse_expression(list(x.replace(" ", "")))[0] for x in instr.strip().split("\n")
    ]

    sigma = 0

    for expression in expressions:
        sigma += calculate(expression)

    return sigma
