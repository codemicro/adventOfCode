# This file is a proof of concept for using the implementation in part one to complete part two
# after added extra brackets to evert expression.

import partOne

instr = open("../input.txt").read()
expressions = instr.strip().split("\n")

expressions = [
    partOne.parse_expression(
        list(("( " + x.replace("*", ") * (") + " )").replace(" ", ""))
    )[0]
    for x in instr.strip().split("\n")
]

sigma = 0

for expression in expressions:
    sigma += partOne.calculate(expression)

print(sigma)
