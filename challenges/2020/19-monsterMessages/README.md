# [Day 19: Monster Messages](https://adventofcode.com/2020/day/19)

Regex, but this time it's not actually too much of a problem.

### Part one

The set of rules that our challenge input provides can pretty easily be parsed and converted into regular expressions, which we can use along with our language's built in regex package in order to parse and validate each message in our input.

### Part two

Part two is also done with regular expressions, however they are modified after they are generated. Since there are only two rules that have recursive properties, conditions for each are hardcoded into the script.

If the recursive rule is rule number `8`, a plus sign is added after the rule for `42`, to denote that sequence can be present one or more times.

If the recursive rule is rule number `11`, a marker is added in place of the full regular expression. When the rest of the rule has been entirely generated, rule 11 is generated alone. This is then put in the marker in the original regular expression. Since this will add another marker, this replacement is repeated 10 times.

The regular expression can then be compared against the messages as in part one.

<details><summary>Script output</summary>

```
❯ python .\python\
AoC 2020: day 19 - Monster Messages
Python 3.8.5

Test cases
1.1 pass
2.1 pass

Answers
Part 1: 222
Part 2: 339

❯ go run .\go\
AoC 2020: day 19 - Monster Messages
Go go1.15.2

Test cases
1.1 pass
2.1 pass

Answers
Part 1: 222
Part 2: 339
```

</details>
