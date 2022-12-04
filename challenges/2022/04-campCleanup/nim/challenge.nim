import std/strutils
import std/sequtils
import std/re
import std/sets


type
    ElfTaskRange = (int, int)
    ElfPair = (ElfTaskRange, ElfTaskRange)

let parseRe = re(r"(\d+)-(\d+),(\d+)-(\d+)")


proc parse(instr: string): seq[ElfPair] =
    for ep in instr.strip().splitlines():
        var matches: array[4, string]
        if not match(ep, parseRe, matches):
            raise newException(ValueError, "badly formed input line '" & ep & "'")

        let intMatches = matches.map(parseInt)
        result.add((
            (intMatches[0], intMatches[1]),
            (intMatches[2], intMatches[3]),
        ))
        

proc makeSet(tr: ElfTaskRange): HashSet[int] = 
    return (tr[0]..tr[1]).toSeq.toHashSet


proc count(inp: seq[ElfPair], pred: proc(a, b: HashSet[int], lenIntersection: int): bool): int =
    for pair in inp:
        let
            a = makeSet(pair[0])
            b = makeSet(pair[1])
            intsn = intersection(a, b)

        if pred(a, b, intsn.len):
            result += 1



proc partOne*(instr: string): int =
    let inp = parse(instr)
    return count(inp, proc (a, b: HashSet[int], i: int): bool =
        i == len(a) or i == len(b)
    )

proc partTwo*(instr: string): int =
    let inp = parse(instr)
    return count(inp, proc (a, b: HashSet[int], i: int): bool =
        return i != 0
    )