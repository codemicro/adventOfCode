import std/strutils
import std/tables
import std/sequtils

type Match = (char, char)

const
    rock = 'A'
    paper = 'B'
    scissors = 'C'

    lose = 'X'
    draw = 'Y'
    win = 'Z'

    scores = {
        rock: 1,
        paper: 2,
        scissors: 3,

        win: 6,
        lose: 0,
        draw: 3,
    }.toTable

    magicBeans = [scissors, rock, paper, scissors, rock].toSeq

    outcomeOffsets = {
        win: 1,
        lose: -1,
        draw: 0,
    }.toTable

proc indexOf[T](x: seq[T], v: T): int = indexOf(x, v, 0, x.len)

proc indexOf[T](x: seq[T], v: T, start: int): int = indexOf(x, v, start, x.len)

proc indexOf[T](x: seq[T], v: T, start: int, stop: int): int =
    for i in start..<stop:
        if x[i] == v:
            return i
    raise newException(ValueError, "item not found in supplied sequence")

proc parse(instr: string): seq[Match] =
    for x in instr.strip.splitlines():
        result.add((x[0], x[2]))

proc partOne*(instr: string): int =
    var inp = parse(instr)

    for i in 0..<inp.len:
        inp[i][1] = case inp[i][1]:
            of 'X':
                rock
            of 'Y':
                paper
            of 'Z':
                scissors
            else:
                raise newException(ValueError, "unknown value " & $inp[i][1])

    for m in inp:
        result += scores[m[1]]

        if m[0] == m[1]:
            result += scores[draw]
        else:
            let opponent = magicBeans.indexOf(m[1], 1)
            let ours = magicBeans.indexOf(m[0], opponent - 1, opponent + 2)

            if opponent - ours == outcomeOffsets[win]:
                result += scores[win]

proc partTwo*(instr: string): int =
    let inp = parse(instr)

    for m in inp:
        result += scores[m[1]]
        let our_move = magicBeans[magicBeans.indexOf(m[0], 1) + outcomeOffsets[
                m[1]]]
        result += scores[our_move]
