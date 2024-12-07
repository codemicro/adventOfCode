# [Day 6: Guard Gallivant](https://adventofcode.com/2024/day/6)

Part 2 is:
* higher than 456
* less than 1689

The first implementation of part 2 took 15 minutes to run.

* Turning `visited_sequence` in `trace` into a set instead of a list cut this to 60 seconds
* Starting immediately in front of the new obstacle when testing positions to put said new obstacle in cut this to 20 seconds
* Removing a load of maps and type wranging to turn the fully generic `gridutil.add` (and counterparts) into a more limited but much faster function took this to ~16 seconds

Before:

```py
def _coordmap(a: AnyCoordinate, b: AnyCoordinate, fn: Callable) -> AnyCoordinate:
    at = type(a)
    return at(*map(fn, zip(a, b)))

def add(a: AnyCoordinate, b: AnyCoordinate) -> AnyCoordinate:
    return _coordmap(a, b, lambda x: x[0] + x[1])
```

After:


```py
def add(a: Coordinate, b: Coordinate) -> Coordinate:
    return Coordinate(a.x + b.x, a.y + b.y)
```