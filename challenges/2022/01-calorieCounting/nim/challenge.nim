import std/strutils
import std/sequtils
import std/algorithm

proc parseInput(instr: string): seq[seq[int]] =
    result = instr.
        strip.
        split("\n\n").
        map(proc(x: string): seq[int] = x.splitLines.map(parseInt))

proc sum(x: openArray[int]): int =
    for i in 0..<x.len:
        result += x[i]

proc partOne*(instr: string): int =
    let input = parseInput(instr)
    var x: seq[int]

    for i in 0..<input.len:
        var sum: int
        for y in 0..<input[i].len:
            sum += input[i][y]
        x.add(sum)

    return max(x)

proc partTwo*(instr: string): int =
    let input = parseInput(instr)
    var x: seq[int]

    for i in 0..<input.len:
        var sum: int
        for y in 0..<input[i].len:
            sum += input[i][y]
        x.add(sum)

    x.sort(SortOrder.Descending)

    return sum(x[0..2])
