Coordinate = tuple[int, int]


def add(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def sub(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return xa - xb, ya - yb
