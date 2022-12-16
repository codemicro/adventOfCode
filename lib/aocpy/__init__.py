from __future__ import annotations
from typing import Any, TypeVar, Callable, Iterable


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

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

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
        return hash(f"{self.x},{self.y}")
