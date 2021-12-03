import std/sequtils
import std/strformat
import std/strutils

proc parse(instr: string): tuple[numbers: seq[int], length: int] =
    let y = instr.splitLines.filter(proc(x: string): bool = x != "")
    return (y.map(parseBinInt), y[0].len)

proc getBit(number: int, n: int): int = 
    return (number shr n) and 0b1

proc analyseBits(numbers: seq[int], n: int): tuple[mostCommon, leastCommon: int] =
    var
        zeros = 0
        ones = 0
    
    for _, number in numbers:
        let sel = getBit(number, n)
        case sel
        of 0:
            zeros += 1
        of 1:
            ones += 1
        else:
            raise newException(ValueError, fmt"impossible value {sel} reached")

    if zeros > ones:
        return (0, 1)
    elif ones > zeros:
        return (1, 0)
    return (-1, -1)

proc partOne*(instr: string): int =
    let (numbers, bitLength) = parse(instr)
    
    var gamma, epsilon: string

    for bitNumber in countdown(bitLength-1, 0):
        let (mostCommon, leastCommon) = analyseBits(numbers, bitNumber)
        gamma.add($mostCommon)
        epsilon.add($leastCommon)

    return parseBinInt(gamma) * parseBinInt(epsilon)

proc partTwo*(instr: string): int =
    let (numbers, bitLength) = parse(instr)

    proc find(inp: seq[int], useMostCommon: bool, n: int = bitLength-1): int =
        if inp.len == 1:
            return inp[0]

        let (mostCommon, leastCommon) = analyseBits(inp, n)

        var target: int
        if mostCommon == -1 or leastCommon == -1:
            if useMostCommon:
                target = 1
            else:
                target = 0
        else:
            if useMostCommon:
                target = mostCommon
            else:
                target = leastCommon

        return find(
            inp.filter(
                proc(x: int): bool = getBit(x, n) == target,
            ),
            useMostCommon,
            n-1
        )

    let
        o2Rating = find(numbers, true)
        co2Rating = find(numbers, false)

    return o2Rating * co2Rating