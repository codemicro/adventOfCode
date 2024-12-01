from enum import Enum, auto
from collections import namedtuple
from numbers import Number
from typing import TypeVar, Callable, Union


Coordinate = namedtuple("Coordinate", ["x", "y"])
Coordinate3 = namedtuple("Coordinate3", ["x", "y", "z"])
AnyCoordinate = Coordinate | Coordinate3


def _coordmap(a: AnyCoordinate, b: AnyCoordinate, fn: Callable) -> AnyCoordinate:
    at = type(a)
    return at(*map(fn, zip(a, b)))


def add(a: AnyCoordinate, b: AnyCoordinate) -> AnyCoordinate:
    return _coordmap(a, b, lambda x: x[0] + x[1])


def sub(a: AnyCoordinate, b: AnyCoordinate) -> AnyCoordinate:
    return _coordmap(a, b, lambda x: x[0] - x[1])


def mult(a: AnyCoordinate, b: Number) -> AnyCoordinate:
    at = type(a)
    return at(*map(lambda x: x * b, a))


def manhattan_dist(a: AnyCoordinate, b: AnyCoordinate) -> Number:
    return sum(map(abs, sub(b, a)))
    

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
        if type(x) != Direction:
            return False
        return self.value == x.value

    def __hash__(self):
        return hash(self.value)