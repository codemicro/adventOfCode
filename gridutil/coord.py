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


def manhattan_dist(a: Coordinate, b: Coordinate) -> Coordinate:
    x, y = sub(b, a)
    return abs(x) + abs(y)


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
    
    def __lt__(self, x):
        return False

    def __eq__(self, x):
        return self.value == x.value

    def __hash__(self):
        return hash(self.value)