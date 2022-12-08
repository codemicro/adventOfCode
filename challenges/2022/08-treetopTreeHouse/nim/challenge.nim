import std/tables
import std/strutils
import std/sequtils

type
    Coordinate = (int, int)
    Forest = ref Table[Coordinate, int]

proc parse(instr: string): (Forest, Coordinate) =
    var forest = newTable[Coordinate, int]()
    
    let lines = instr.strip().splitlines()

    var
        x = 0
        y = 0

    while x < lines.len:
        y = 0
        while y < lines[x].len:
            forest[(x, y)] = parseInt($lines[x][y])
            y += 1
        x += 1
    
    return (forest, (x, y))

proc areAdjacentsLower(forest: Forest, initialPos: Coordinate, nextPos: proc(pos: Coordinate): Coordinate): bool = 
    let height = forest[initialPos]
    var pos = nextPos(initialPos)
    while forest.contains(pos):
        if forest[pos] >= height:
            return false
        pos = nextPos(pos)
    return true

proc getViewingDistance(forest: Forest, initialPos: Coordinate, nextPos: proc(pos: Coordinate): Coordinate): int = 
    let height = forest[initialPos]
    var pos = nextPos(initialPos)
    while forest.contains(pos):
        result += 1
        if forest[pos] >= height:
            break  
        pos = nextPos(pos)

proc partOne*(instr: string): int =
    let
        (forest, maxPos) = parse(instr)
        (maxX, maxY) = maxPos

    for treePos in forest.keys():
        let (x, y) = treePos
        if x == 0 or y == 0 or x == maxX or y == maxY:
            result += 1
            continue

        if areAdjacentsLower(forest, treePos, proc(c: Coordinate): Coordinate = (c[0] - 1, c[1])):
            result += 1
            continue

        if areAdjacentsLower(forest, treePos, proc(c: Coordinate): Coordinate = (c[0] + 1, c[1])):
            result += 1
            continue

        if areAdjacentsLower(forest, treePos, proc(c: Coordinate): Coordinate = (c[0], c[1] - 1)):
            result += 1
            continue

        if areAdjacentsLower(forest, treePos, proc(c: Coordinate): Coordinate = (c[0], c[1] + 1)):
            result += 1


proc partTwo*(instr: string): int =
    let (forest, _) = parse(instr)

    for treePos in forest.keys():
        let
            view_left = getViewingDistance(forest, treePos, proc(c: Coordinate): Coordinate = (c[0] - 1, c[1]))
            view_right = getViewingDistance(forest, treePos, proc(c: Coordinate): Coordinate = (c[0] + 1, c[1]))
            view_up = getViewingDistance(forest, treePos, proc(c: Coordinate): Coordinate = (c[0], c[1] - 1))
            view_down = getViewingDistance(forest, treePos, proc(c: Coordinate): Coordinate = (c[0], c[1] + 1))

        let senic = view_left * view_right * view_up * view_down
        if senic > result:
            result = senic
