import std/sets

proc find_unique_sequence(instr: string, length: int): int =
    for i in countup(0, instr.len - length):
        if toHashSet(instr[i..<i+length]).len == length:
            return i+length
    raise newException(ValueError, "cannot solve")

proc partOne*(instr: string): int = find_unique_sequence(instr, 4)

proc partTwo*(instr: string): int = find_unique_sequence(instr, 14)
