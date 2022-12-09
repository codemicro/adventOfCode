import std/strutils
import std/tables

type
    Vector = (int, int)
    Instruction = (char, int)

const
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

    OFFSETS = {
        RIGHT: (1, 0),
        LEFT: (-1, 0),
        UP: (0, 1),
        DOWN: (0, -1),
    }.toTable()
    
proc parse(instr: string): seq[Instruction] = 
    for x in instr.strip().splitlines():
        result.add((x[0], parseInt(x[2..<x.len])))

proc `+`(a, b: Vector): Vector = 
    return (a[0] + b[0], a[1] + b[1])

proc `-`(a, b: Vector): Vector =
    return (a[0] - b[0], a[1] - b[1])

proc getNextMoveDelta(currentPosition, preceedingPosition: Vector): Vector =
    let (dx, dy) = preceedingPosition - currentPosition

    if -1 <= dx and dx <= 1 and -1 <= dy and dy <= 1:
        return (0, 0)

    if dy > 0 and dx == 0:
        # head upwards of tail
        return OFFSETS[UP]
    elif dy < 0 and dx == 0:
        # head downwards of tail
        return OFFSETS[DOWN]
    elif dy == 0 and dx > 0:
        # head to the right of tail
        return OFFSETS[RIGHT]
    elif dy == 0 and dx < 0:
        # head to the left of tail
        return OFFSETS[LEFT]
    elif dy > 0 and dx > 0:
        # head diagonally up-right of the tail
        return OFFSETS[UP] + OFFSETS[RIGHT]
    elif dy > 0 and dx < 0:
        # head diagonally up-left of the tail
        return OFFSETS[UP] + OFFSETS[LEFT]
    elif dy < 0 and dx > 0:
        # head diagonally down-right of the tail
        return OFFSETS[DOWN] + OFFSETS[RIGHT]
    elif dy < 0 and dx < 0:
        # head diagonally down-left of the tail
        return OFFSETS[DOWN] + OFFSETS[LEFT]

    return (0, 0)

proc runWithLength(instructions: seq[Instruction], ropeLength: int): int =
    var 
        positions: seq[Vector] = newSeq[Vector](ropeLength)
        tailVisited: Table[Vector, int] = {(0, 0): 0}.toTable()

    for (direction, magnitude) in instructions:
        for _ in countup(0, magnitude - 1):
            positions[0] = positions[0] + OFFSETS[direction]

            var delta: Vector
            for posNum in countup(1, positions.len - 1):
                delta = getNextMoveDelta(positions[posNum], positions[posNum-1])
                if delta == (0, 0):
                    break

                positions[posNum] = positions[posNum] + delta

            if delta == (0, 0):
                continue

            let last = positions[positions.len-1]
            if not tailVisited.contains(last):
                tailVisited[last] = 0

    return len(tailVisited)

proc partOne*(instr: string): int =
    return runWithLength(parse(instr), 2)

proc partTwo*(instr: string): int =
    return runWithLength(parse(instr), 10)