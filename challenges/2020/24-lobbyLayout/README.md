# [Day 24: Lobby Layout](https://adventofcode.com/2020/day/24)

More cellular automata! Just this time, weird. Perhaps even weirder than [day 17](../17-conwayCubes). Hexagonal cells broke my brain a pretty substantial amount.

[This StackOverflow answer](https://stackoverflow.com/a/7393897) proved pretty crucial to me ending up solving the challenge. To summarise:

We can represent our flooring using a typical 2D array, provided we visualise it with each line offset by a constant amount from the previous like so:

```
(0,0) (0,1) (0,2) (0,3) (0,4)

   (1,0) (1,1) (1,2) (1,3) (1,4)

      (2,0) (2,1) (2,2) (2,3) (2,4)

         (3,0) (3,1) (3,2) (3,3) (3,4)
```

The six neighbours to a given cell form what I believe called a slanted neighbourhood.

Using this, we can find a series of vectors that represent `e`, `se`, `sw`, `w`, `nw`, and `ne` directions from a specific tile.

```
(r, s) current tile

(r-1, s) nw
(r-1, s+1) ne
(r, s-1) w
(r, s+1) e
(r+1, s-1) sw
(r+1, s) se
```

From here onwards, it's pretty simple to solve the rest of the challenge.

### Related

* [Wikipedia - Cellular automata](https://en.wikipedia.org/wiki/Cellular_automaton)
* [Tim Hutton - A Slanted Hexagon](https://ferkeltongs.livejournal.com/31455.html)
* [StackOverflow - What's the best way to represent a hexagonal lattice?](https://stackoverflow.com/a/7393897)

<details><summary>Script output</summary>

```
❯ python .\python\ ft
AoC 2020: day 24 - Lobby Layout
Python 3.8.5

Test cases
1.1 pass in 0.0004611015319824219 seconds
2.1 pass in 0.6723911762237549 seconds

Answers
Part 1: 497 in 0.004002571105957031 seconds
Part 2: 4156 in 1.6635417938232422 seconds
```

</details>
