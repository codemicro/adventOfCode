# [Day 7: Bridge Repair](https://adventofcode.com/2024/day/7)

Part 1 is:
* greater than 450054910499

Before optimisation (pregenerating then testing operator combiantions using `itertools.product("*+|", length=n)`), run time looks something like this:

```
Part 1: min 0.2671 seconds, max 0.2818 seconds, avg 0.2755
Part 2: min 23.2387 seconds, max 24.8753 seconds, avg 23.8805
```

It also appeared that using string concatenation as opposed to pure mathematical functions for the concatenation operator was marginally faster in Python.

After optimisation (recursive solves working backwards through the numbers), the run time looks something like this:

```
Part 1: min 0.0214 seconds, max 0.041 seconds, avg 0.0233
Part 2: min 0.0215 seconds, max 0.0273 seconds, avg 0.0229
```

The intial version of this solve is in commit `b2fa4b7`.