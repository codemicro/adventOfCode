import std/sets
import std/strutils

proc parse(instr: string): seq[string] = instr.strip.splitlines

proc getPriority(ch: char): int =
    let co = ch.ord
    if ord('a') <= co and co <= ord('z'):
        return (co - ord('a')) + 1
    return (co - ord('A')) + 27

proc partOne*(instr: string): int =
    let inp = parse(instr)

    var sigma = 0
    for x in inp:
        assert x.len mod 2 == 0
        let l = x.len div 2
        var y = intersection(
            toHashSet(x[0..<l]),
            toHashSet(x[l..<x.len]),
        )
        sigma += getPriority(y.pop())

    return sigma

proc partTwo*(instr: string): int =
    let inp = parse(instr)
    assert inp.len mod 3 == 0

    var sigma = 0
    for i in countup(0, inp.len - 1, 3):
        var x = toHashSet(inp[i])
        x = intersection(x, toHashSet(inp[i + 1]))
        x = intersection(x, toHashSet(inp[i + 2]))

        sigma += getPriority(x.pop())

    return sigma
