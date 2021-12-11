import std/tables
import std/strutils

type
    Point = (int, int)
    Cave = Table[Point, int]

proc parse(instr: string): Cave =
    for y, line in instr.strip.splitLines[0 .. ^1]:
        for x, digitChar in line.pairs:
            result[(x, y)] = parseInt($digitChar)

proc getAdjacentPoints(point: Point): seq[Point] =
    let (x, y) = point
    return @[
        (x, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y - 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
    ]

proc iterate(cave: Cave): (Cave, int, bool) =
    var cave = cave

    for point in cave.keys:
        cave[point] = cave[point] + 1

    var updates = Cave()
    var hasFlashed: seq[Point]

    proc handleNine(point: Point) =
        updates[point] = 0
        hasFlashed.add(point)
        for adjacent in getAdjacentPoints(point):
            if not (adjacent in cave):
                continue

            var previousValue = cave[adjacent]
            if adjacent in updates:
                previousValue = updates[adjacent]

            updates[adjacent] = previousValue + 1

            if previousValue + 1 > 9 and not (adjacent in hasFlashed):
                handleNine(adjacent)

    for point in cave.keys:
        if cave[point] > 9 and not (point in hasFlashed):
            handleNine(point)

    for point in updates.keys:
        cave[point] = updates[point]

    for point in hasFlashed:
        cave[point] = 0

    return (cave, hasFlashed.len, hasFlashed.len == cave.len)


proc partOne*(instr: string): int =
    var cave = parse(instr)

    for _ in countup(1, 100):
        let (c, n, _) = iterate(cave)
        cave = c
        result += n

proc partTwo*(instr: string): int =
    var cave = parse(instr)
    while true:
        result += 1
        let (c, _, allFlashed) = iterate(cave)
        if allFlashed:
            return
        cave = c
