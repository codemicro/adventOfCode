# [Day 13: Point of Incidence](https://adventofcode.com/2023/day/13)

I've got a function that checks vertical lines of symmetry, and to check horizontal ones I just swap the `(x, y)` coords in the grid to `(y, x)` then run it again.

For each candidate line of symmetry, work out a range that values we need to check (based on which side goes out of bounds first), then for each row in the full height of the grid, count how many rocks are `x` steps away from the line (eg. `.#.|.#.` has 2 rocks 1 step away, assuming the pipe is the line we're checking around).

For part 1, we just check that no single row has any step within it that doesn't have 0 or 2 rocks.

For part 2, we make the same check but allow any grid where only a single row fouls that condition. This gives us multiple candidate lines of symmetry for each grid, so we diff it with the as-is case from part 1 and use whatever is new.