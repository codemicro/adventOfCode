from __future__ import annotations
from typing import Any, TypeVar, Callable, Iterable
from collections.abc import Sequence


class BaseChallenge:

    @staticmethod
    def one(instr: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def two(instr: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def vis(instr: str, outputDir: str) -> Any:
        raise NotImplementedError


T = TypeVar("T")
U = TypeVar("U")

def foldl(p: Callable[[U, T], U], i: Iterable[T], start: U) -> U:
    res = start
    for item in i:
        res = p(res, item)
    return res

def foldr(p: Callable[[U, T], U], i: Iterable[T], start: U) -> U:
    return foldl(p, reversed(i), start)


class Vector:
    x: int
    y: int

    def __init__(self, *args):
        if len(args) == 1 and Vector._is_vector_tuple(args[0]):
            x, y = args[0]
        elif len(args) != 2:
            return ValueError("expected integer tuple or pair of integers")
        else:
            x, y = args
        
        self.x = int(x)
        self.y = int(y)

    @staticmethod
    def _is_vector_tuple(o: Any) -> bool:
        return type(o) == tuple and len(o) == 2 and type(o[0]) == int and type(o[1]) == int

    def manhattan_distance(self, o: Vector) -> int:
        return abs(self.x - o.x) + abs(self.y - o.y)

    def __add__(self, o: Any) -> Vector:
        if Vector._is_vector_tuple(o):
            return Vector(self.x + o[0], self.y + o[1])
        elif type(o) == Vector:
            return Vector(self.x + o.x, self.y + o.y)
        else:
            raise ValueError(f"cannot add Vector and {type(o)}")

    def __sub__(self, o: Any) -> Vector:
        if Vector._is_vector_tuple(o):
            return Vector(self.x - o[0], self.y - o[1])
        elif type(o) == Vector:
            return Vector(self.x - o.x, self.y - o.y)
        else:
            raise ValueError(f"cannot subtract Vector and {type(o)}")

    def __eq__(self, o: Any) -> bool:
        if Vector._is_vector_tuple(o):
            return self.x == o[0] and self.y == o[1]
        elif type(o) == Vector:
            return self.x == o.x and self.y == o.y
        else:
            raise ValueError(f"cannot equate Vector and {type(o)}")

    def __repr__(self) -> str:
        # return f"Vector(x={self.x}, y={self.y})"
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

class Consumer:
    x: Sequence[T]
    i: int

    def __init__(self, x: Sequence[T]):
        self.x = x
        self.i = 0
    
    def take(self) -> T:
        self.i += 1
        return self.x[self.i-1]

    def undo(self):
        self.i -= 1

class RepeatingConsumer(Consumer):
    def take(self) -> T:
        val = super().take()
        self.i = self.i % len(self.x)
        return val

    def undo(self):
        super().undo()
        if self.i < 0:
            self.i += len(self.x)