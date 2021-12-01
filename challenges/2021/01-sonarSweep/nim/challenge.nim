import std/strutils
import std/sequtils

proc loadInput(): string =
    return readFile("input.txt")

proc parseInput(instr: string): seq[int] =
    for item in split(instr, "\n"):
        if item == "":
            continue
        let n = parseInt(item)
        result.add(n)

let input = parseInput(loadInput())

proc countIncreases(data: seq[int]): int = 
    for i in countup(1, data.len()-1):
        if data[i] > data[i-1]:
            result = result + 1

proc partOne(): int =
    return countIncreases(input)

proc partTwo(): int =
    var sums: seq[int]
    for i in countup(0, len(input)-3):
        sums.add(
            (@input[i..i+2]).foldl(a+b),
        )
    return countIncreases(sums)

echo "Part one: " & $partOne()
echo "Part two: " & $partTwo()