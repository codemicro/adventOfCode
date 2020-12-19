# [Day 18: Operation Order](https://adventofcode.com/2020/day/18)

### Part one

Each expression is represented by a list. Each set of brackets in an input is a nested list within that list. For example:

```py
>>> parse_expression("1 + 1 + (3 * 4) + 8".replace(" ", ""))[0]
['1', '+', '1', '+', ['3', '*', '4'], '+', '8']
```

In order to calculate this, a recursive function is used to step through each item and perform any operations found in a linear manner (ie, ignoring [operator precedence](https://en.wikipedia.org/wiki/Order_of_operations)).

### Part two

Attempts to use the same data structure for part two, while possible, were difficult and I never actually ended up getting any of them working. I tried two different methods.

* Encasing every single addition operation in a set of brackets (this was done after parsing, so it was actually replacing three items from a list with a list of those three items)
* Selectivley calculating only the additions in an expression before then going on to calculate the multiplication
  * This isn't actually possible - how are you meant to calculate `1 + (2 + 3 * 4)` without multiplication?

After I started wanting to punch myself repeatedly in the head because of the amount of issues I was having with my own solution, I gave up and found an implentation of the shunting-yard algorithm ([this one](http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html), to be precise), modified the operator precendences and used that.

It worked first try. *sigh*

At some point, I'd like to come back to this and write my own implementation, and convert the first part to using that new implementation.

### Related

* [Wikipedia - Shunting-yard algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm)
* [Computerphile - Reverse Polish Notation and The Stack](https://www.youtube.com/watch?v=7ha78yWRDlE)

<details><summary>Script output</summary>

```
❯ python .\python\
AoC 2020: day 18 - Operation Order
Python 3.8.5

Test cases
1.1 pass
1.2 pass
1.3 pass
1.4 pass
1.5 pass
1.6 pass
2.1 pass
2.2 pass
2.3 pass
2.4 pass
2.5 pass
2.6 pass

Answers
Part 1: 18213007238947
Part 2: 388966573054664
```

</details>
