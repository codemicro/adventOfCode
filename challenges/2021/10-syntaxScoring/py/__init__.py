from typing import List, Optional, Tuple
from aocpy import BaseChallenge
from dataclasses import dataclass
import math
from collections import deque


CHECKER_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

AC_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


@dataclass
class Chunk:
    text: str

    def is_corrupted(self) -> Tuple[bool, Optional[str]]:
        stack = deque()
        for char in self.text:

            if char == "(":
                stack.append(")")
            elif char == "[":
                stack.append("]")
            elif char == "{":
                stack.append("}")
            elif char == "<":
                stack.append(">")
            elif char == ")" or char == "]" or char == "}" or char == ">":
                r = stack.pop()
                if r != char:
                    return True, char
            else:
                raise ValueError(f"unknown character in chunk string ({char=})")

        return False, None

    def complete(self) -> str:
        stack = deque()
        output = ""

        n = 0
        while True:

            char = None
            if n < len(self.text):
                char = self.text[n]

            if len(stack) == 0 and char is None:
                break

            if char is None:
                output += stack.pop()
            elif char == "(":
                stack.append(")")
            elif char == "[":
                stack.append("]")
            elif char == "{":
                stack.append("}")
            elif char == "<":
                stack.append(">")
            elif char == ")" or char == "]" or char == "}" or char == ">":
                r = stack.pop()
                if r != char:
                    raise ValueError(
                        f"cannot correct corrupted chunk (wanted {r}, got {char})"
                    )
            else:
                raise ValueError(f"unknown character in chunk string ({char=})")

            n += 1

        return output


def parse(instr: str) -> List[Chunk]:
    return [Chunk(x) for x in instr.strip().splitlines()]


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        chunks = parse(instr)
        score = 0
        for chunk in chunks:
            is_corrupted, illegal_character = chunk.is_corrupted()
            if is_corrupted:
                score += CHECKER_POINTS[illegal_character]
        return score

    @staticmethod
    def two(instr: str) -> int:
        chunks = parse(instr)

        def f(x):
            y, _ = x.is_corrupted()
            return not y

        chunks = list(filter(f, chunks))
        points = []
        for chunk in chunks:
            extra = chunk.complete()
            n = 0
            for char in extra:
                n *= 5
                n += AC_POINTS[char]
            points.append(n)

        points = list(sorted(points))
        median = points[math.floor(len(points) / 2)]

        return median
