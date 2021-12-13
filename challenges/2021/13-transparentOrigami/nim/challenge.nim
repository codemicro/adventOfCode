import std/tables
import std/strutils
import std/sequtils

type
    Point = (int, int)
    Sheet = Table[Point, bool]
    Instruction = object
        axis: string
        n: int

proc parse(instr: string): (Sheet, seq[Instruction]) =
    let
        sp = instr.strip.split("\n\n")
        sheetPoints = sp[0]
        rawInstructions = sp[1]

    var sheet = Sheet()
    for point in sheetPoints.splitlines:
        let x = point.split(",")
        sheet[(parseInt(x[0]), parseInt(x[1]))] = true

    var instructions: seq[Instruction]
    for line in rawInstructions.splitlines:
        let x = line.split(" ")[^1].split("=")
        instructions.add(Instruction(axis: x[0], n: parseInt(x[1])))

    return (sheet, instructions)

proc print(sheet: Sheet) =
    let
        keysSeq = toSeq(sheet.keys)
        maxX = max(map(keysSeq, (proc(p: Point): int = p[0])))
        maxY = max(map(keysSeq, (proc(p: Point): int = p[1])))

    var lines: seq[string]

    for y in 0..maxY:
        var ll: string
        for x in 0..maxX:
            if sheet.hasKey((x, y)):
                ll.add("██")
            else:
                ll.add("  ")
        lines.add(ll)

    for x in lines:
        echo x

proc applyInstruction(sheet: Sheet, instruction: Instruction): Sheet =
    for p in sheet.keys:
        var v: int
        case instruction.axis
        of "x":
            v = p[0]
        of "y":
            v = p[1]
        else:
            raise newException(ValueError, "unknown axis")

        if v > instruction.n:
            if instruction.axis == "x":
                result[(instruction.n - (p[0] - instruction.n), p[1])] = true
            else: # assume y
                result[(p[0], instruction.n - (p[1] - instruction.n))] = true
        else:
            result[p] = true

proc partOne*(instr: string): int =
    var (sheet, instructions) = parse(instr)
    sheet = apply_instruction(sheet, instructions[0])
    return sheet.len

proc partTwo*(instr: string): string =
    var (sheet, instructions) = parse(instr)
    for instruction in instructions:
        sheet = applyInstruction(sheet, instruction)
    sheet.print
    return "work it out yourself"
