from enum import Enum
from typing import *
from aocpy import BaseChallenge


class State(Enum):
    EMPTY = None
    WALL = 1
    SAND = 2


Vector = Tuple[int, int]
Scan = Dict[Vector, State]


def parse(instr: str) -> Tuple[Scan, Vector, Vector]:
    res = {}

    for line in instr.strip().splitlines():
        points: List[Vector] = []
        for x in line.split("->"):
            p = x.split(",")
            points.append((int(p[0]), int(p[1])))

        for i in range(len(points) - 1):
            next_i = i + 1
            dx = points[next_i][0] - points[i][0]
            dy = points[next_i][1] - points[i][1]

            # If either dx or dy is positive, that means its going down or left respectively

            assert dx == 0 or dy == 0

            if dx == 0:
                f = lambda x, y: x + y
                if dy < 0:
                    f = lambda x, y: x - y

                for j in range(abs(dy) + 1):
                    res[(points[i][0], f(points[i][1], j))] = State.WALL
            else:
                f = lambda x, y: x + y
                if dx < 0:
                    f = lambda x, y: x - y

                for j in range(abs(dx) + 1):
                    res[(f(points[i][0], j), points[i][1])] = State.WALL

    keys = res.keys()
    min_x = min(keys, key=lambda x: x[0])[0]
    max_x = max(keys, key=lambda x: x[0])[0]
    min_y = min(keys, key=lambda x: x[1])[1]
    max_y = max(keys, key=lambda x: x[1])[1]

    return res, (min_x, min_y), (max_x, max_y)


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp, min_pos, max_pos = parse(instr)

        cursor = (500, 0)
        grains = 0

        while (min_pos[0] <= cursor[0] <= max_pos[0]) and (
            0 <= cursor[1] <= max_pos[1]
        ):
            x, y = cursor

            if inp.get((x, y + 1)) is None:
                cursor = (x, y + 1)
            elif inp.get((x, y + 1)) == State.WALL or inp.get((x, y + 1)) == State.SAND:
                if inp.get((x - 1, y + 1)) is None:
                    cursor = (x - 1, y + 1)
                elif inp.get((x + 1, y + 1)) is None:
                    cursor = (x + 1, y + 1)
                else:
                    inp[cursor] = State.SAND
                    grains += 1
                    cursor = (500, 0)
            else:
                inp[cursor] = State.SAND
                grains += 1
                cursor = (500, 0)

        return grains

    @staticmethod
    def two(instr: str) -> int:
        inp, _, max_pos = parse(instr)

        max_pos = (max_pos[0], max_pos[1] + 2)

        cursor = (500, 0)
        grains = 0

        def get(k: Vector):
            if k[1] == max_pos[1]:
                return State.WALL

            return inp.get(k)

        while True:
            x, y = cursor

            if get((x, y + 1)) is None:
                cursor = (x, y + 1)
            elif get((x, y + 1)) == State.WALL or get((x, y + 1)) == State.SAND:
                if get((x - 1, y + 1)) is None:
                    cursor = (x - 1, y + 1)
                elif get((x + 1, y + 1)) is None:
                    cursor = (x + 1, y + 1)
                else:
                    inp[cursor] = State.SAND
                    grains += 1
                    if cursor == (500, 0):
                        break
                    cursor = (500, 0)
            else:
                inp[cursor] = State.SAND
                grains += 1
                if cursor == (500, 0):
                    break
                cursor = (500, 0)

        return grains
