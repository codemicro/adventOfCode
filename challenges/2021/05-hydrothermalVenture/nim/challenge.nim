import std/tables
import std/sequtils
import std/strutils

type
    Point = object
        x: int
        y: int

    Line = (Point, Point)


proc pointFromString(instr: string): Point =
    let
        parts = instr.split(",")
        x = parts[0].parseInt
        y = parts[1].parseInt

    return Point(x: x, y: y)

proc parse(instr: string): seq[Line] =
    for line in instr.strip.splitLines:
        let parts = line.split(" -> ")
        result.add((
            pointFromString(parts[0]), pointFromString(parts[1])
        ))

proc removeDiagonalLines(lines: seq[Line]): seq[Line] =
    return lines.filter(
        proc(line: Line): bool = line[0].x == line[1].x or line[0].y == line[
                1].y,
    )

iterator iteratePoints(line: Line): Point =
    let
        (p1, p2) = line
        deltaX = p2.x - p1.x
        deltaY = p2.y - p1.y

    var
        xStep: int
        yStep: int

    if deltaX > 0:
        xStep = 1
    elif deltaX < 0:
        xStep = -1

    if deltaY > 0:
        yStep = 1
    elif deltaY < 0:
        yStep = -1

    var lastPoint = p1
    yield p1
    while lastPoint != p2:
        let np = Point(
            x: lastPoint.x + xStep,
            y: lastPoint.y + yStep,
        )
        yield np
        lastPoint = np

proc countOverlappingPoints(lines: seq[Line]): int =
    var areas = initTable[Point, int]()
    for line in lines:
        for point in iteratePoints(line):
            let nextValue = areas.getOrDefault(point, 0) + 1
            areas[point] = nextValue

    for count in areas.values:
        if count > 1:
            result += 1

proc partOne*(instr: string): int =
    return instr.
        parse.
        removeDiagonalLines.
        countOverlappingPoints

proc partTwo*(instr: string): int =
    return instr.
        parse.
        countOverlappingPoints
