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