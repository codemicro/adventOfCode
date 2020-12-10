# [Day 10: Adapter Array](https://adventofcode.com/2020/day/10)

## Part two explaination

If you take away all the extra details, all we're being asked to do in part two is to find the number of valid possible orderings of the list of joltages where a given ordering is valid if:

* it starts at zero and ends at 3 more than the highest input value
* each value in the input is followed by a value that is between 1 and 3 more than itself
  * for example, if your value was `5`, it could be followed by `6`, `7`, or `8` only.
  * this also means that the value `5` can only be preceded by `2`, `3` or `4`.

We do not need to use all values from the input like we did in part one.

The number of valid combinations to reach value `n` is the sum of the number of valid combinations of `n-1`, `n-2` and `n-3`, assuming values are sorted in ascending order. If one of these numbers is not present in the input, it can be treated as zero.

Where `n` is `0`, there is only one way to combine a single number, hence it has a combinations value of 1.

For example, if we have the following data:

| n | Combinations  |
|---|---------------|
| 0 | 1             |
| 1 | 1             |
| 2 | 2             |

We can find the number of valid combinations to get to the value `n=3` by doing `1 + 1 + 2 = 4`.

Using this method, we can find the answer to part two with a very small algorithm that's only 7 lines long, excluding data parsing.

---

<details><summary>Script output</summary>

```
❯ python .\python\
AoC 2020: day 10 - Adapter Array
Python 3.8.5

Test cases
1.1 pass
1.2 pass
2.1 pass
2.2 pass

Answers
Part 1: 3000
Part 2: 193434623148032

❯ go run .\go\
AoC 2020: day 10 - Adapter Array
Go go1.15.2

Test cases
1.1 pass
1.2 pass
2.1 pass
2.2 pass

Answers
Part 1: 3000
Part 2: 193434623148032
```

</details>
