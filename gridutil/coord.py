from enum import Enum, auto


Coordinate = tuple[int, int]


def add(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def sub(a: Coordinate, b: Coordinate) -> Coordinate:
    xa, ya = a
    xb, yb = b
    return xa - xb, ya - yb


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    def delta(self) -> Coordinate:
        match self:
            case Direction.Up:
                return (0, -1)
            case Direction.Down:
                return (0, 1)
            case Direction.Left:
                return (-1, 0)
            case Direction.Right:
                return (1, 0)

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