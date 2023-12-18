from enum import Enum, auto
from collections import namedtuple
from numbers import Number


Coordinate = namedtuple("Coordinate", ["x", "y"])


def add(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return Coordinate(xa + xb, ya + yb)


def sub(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return Coordinate(xa - xb, ya - yb)


def mult(a: Coordinate, b: Number) -> Coordinate:
    x, y = a
    return Coordinate(x * b, y * b)


def manhattan_dist(a: Coordinate, b: Coordinate) -> Number:
    x, y = sub(b, a)
    return abs(x) + abs(y)


def area(x: list[Coordinate]) -> Number:
    """
    Finds the area of a closed polygon.
    
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    acc = 0
    for ((ax, ay), (bx, by)) in zip(x, x[1:] + [x[0]]):
        acc += (ax * by) - (bx * ay)
    return acc / 2


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    def delta(self) -> Coordinate:
        match self:
            case Direction.Up:
                return Coordinate(0, -1)
            case Direction.Down:
                return Coordinate(0, 1)
            case Direction.Left:
                return Coordinate(-1, 0)
            case Direction.Right:
                return Coordinate(1, 0)

    def opposite(self):
        match self:
            case Direction.Down:
                return Direction.Up
            case Direction.Up:
                return Direction.Down
            case Direction.Left:
                return Direction.Right
            case Direction.Right:
                return Direction.Left
    
    def __lt__(self, x):
        return False

    def __eq__(self, x):
        return self.value == x.value

    def __hash__(self):
        return hash(self.value)