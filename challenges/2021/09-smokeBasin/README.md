# [Day 9: Smoke Basin](https://adventofcode.com/2021/day/9)

The key to solving part two is knowing that you don't need to itelligently think about the depths of the basins.

Because we know that

> Locations of height `9` do not count as being in any basin, and all other locations will always be part of exactly one basin

we can determine that a given basin is bounded by `9`s or the edge of the board. For example, the sample input looks like this if you remove all digits apart from `9`.

```
--999-----
-9---9-9--
9-----9-9-
-----9---9
9-999-----
```

We can find every lowest point, and work outwards from that point to find the entire basin.

---

[Part two visualisation](partTwo.mp4)

To run the visualisation, use the following command:

```
PYTHONPATH=<path to repo root>/lib python3 -B -c "import py;inp=open('input.txt').read();py.Challenge.vis(inp,'visdir')"
```