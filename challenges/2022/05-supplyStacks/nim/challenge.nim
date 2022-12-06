import std/deques
import std/strutils
import std/sequtils
import std/re

type
    MoveInstruction = object
        n: int
        source: int
        destination: int

    Stack[T] = Deque[T]

let instructionRe = re(r"move (\d+) from (\d+) to (\d+)")

proc parse(instr: string): (seq[Stack[char]], seq[MoveInstruction]) =
    let
        x = instr.split("\n\n")
        rawInitialState = x[0]
        rawInstructions = x[1]

    var stateLines = rawInitialState.splitlines()
    stateLines = stateLines[0..<stateLines.len] # the last line only contains
    # digits that we don't need to look at

    var groupedStateLines: seq[seq[string]]
    for line in stateLines:
        var x: seq[string]
        for i in countup(0, line.len, 4):
            x.add(line[i..<i+3])
        groupedStateLines.add(x)

    var state: seq[Stack[char]]
    for _ in countup(0, groupedStateLines[0].len - 1):
        state.add(Stack[char]())

    for lineNumber in countdown(groupedStateLines.len - 1, 0):
        for i, item in groupedStateLines[lineNumber].pairs():
            if item != "   ":
                state[i].addLast(item[1])

    var instructions: seq[MoveInstruction]
    for line in rawInstructions.strip().splitlines():
        var matches: array[3, string]
        if not match(line, instructionRe, matches):
            raise newException(ValueError, "badly formed input line '" & line & "'")

        let intMatches = matches.map(parseInt)

        instructions.add(MoveInstruction(
            n: intMatches[0],
            source: intMatches[1],
            destination: intMatches[2]
        ))

    return (state, instructions)


proc getTopChars(state: seq[Stack[char]]): string =
    for i in countup(0, state.len-1):
        result = result & $state[i].peekLast()


proc partOne*(instr: string): string =
    var (state, instructions) = parse(instr)

    for instruction in instructions:
        for _ in countup(0, instruction.n-1):
            let x = state[instruction.source - 1].popLast()
            state[instruction.destination - 1].addLast(x)

    return getTopChars(state)

proc partTwo*(instr: string): string =
    var (state, instructions) = parse(instr)

    for instruction in instructions:
        var items: seq[char]
        for _ in countup(0, instruction.n-1):
            items.add(state[instruction.source - 1].popLast())

        for i in countdown(items.len - 1, 0):
            state[instruction.destination - 1].addLast(items[i])

    return getTopChars(state)
