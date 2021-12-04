import std/strutils
import std/sequtils

proc parseInput(instr: string): seq[int] =
    result = instr.
        splitLines.
        toSeq.
        filter(proc(x: string): bool = x != "").
        map(parseInt)

proc countIncreases(data: seq[int]): int =
    for i in 1..data.high:
        if data[i] > data[i-1]:
            result = result + 1

proc partOne*(instr: string): int =
    let input = parseInput(instr)
    return countIncreases(input)

proc partTwo*(instr: string): int =
    let input = parseInput(instr)
    var sums: seq[int]
    for i in countup(0, len(input)-3):
        sums.add(input[i] + input[i+1] + input[i+2])
        # sums.add(
        #     (@input[i..i+2]).foldl(a+b),
        # )
    return countIncreases(sums)
