import std/tables
import std/strutils
import std/sequtils
import std/enumerate

const
    LIT = '#'
    UNLIT = '.'

type
    Point = (int, int)
    Image = Table[Point, char]

proc parse(instr: string): (string, Image) =
    let
        sp = instr.strip.split("\n\n")
        algo = sp[0]
        image = sp[1]

    var imageTable = Image()

    for y, line in enumerate(image.splitLines):
        for x, pixel in line[0..^1]:
            if pixel == LIT:
                imageTable[(x, y)] = pixel

    return (algo, imageTable)


proc getAdjacentPoints(centerPoint: Point): array[0..8, Point] =
    let (x, y) = centerPoint
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]


proc enhanceN(image: Image, algorithm: string, n: int): Image =
    result = image
    for i in 0..<n:
        let
            keysSeq = toSeq(result.keys)
            xVals = map(keysSeq, (proc(p: Point): int = p[0]))
            yVals = map(keysSeq, (proc(p: Point): int = p[1]))

            minX = min(xVals)
            maxX = max(xVals)
            minY = min(yVals)
            maxY = max(yVals)

        var changes = Image()

        for y in minY - 2 ..< maxY + 2:
            for x in minX - 2 ..< maxX + 2:
                let p = (x, y)

                var n: int

                for point in getAdjacentPoints(p):
                    let (px, py) = point
                    var isLit: bool

                    if algorithm[0] == LIT and not (minX <= px and px <=
                            maxX and minY <= py and py <= maxY):
                        isLit = i mod 2 != 0
                    else:
                        isLit = result.getOrDefault(point, UNLIT) == LIT

                    n = n shl 1

                    if isLit:
                        n = n or 0b1

                changes[p] = algorithm[n]

        for point, change in changes.pairs:
            if change == UNLIT and point in result:
                result.del(point)
            elif change == LIT:
                result[point] = LIT

proc core(instr: string, n: int): int =
    let
        parsed = parse(instr)
        algorithm = parsed[0]
    var image = parsed[1]

    image = enhanceN(image, algorithm, n)
    return len(image)

proc partOne*(instr: string): int =
    return core(instr, 2)

proc partTwo*(instr: string): int =
    return core(instr, 50)
