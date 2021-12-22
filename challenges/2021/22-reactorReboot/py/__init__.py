from dataclasses import dataclass
from typing import Any, List, NamedTuple, Generator
from aocpy import BaseChallenge


MODE_ON = "on"
MODE_OFF = "off"


class Point(NamedTuple):
    x: int
    y: int
    z: int


@dataclass
class Shape:
    mode: str
    p1: Point
    p2: Point

    def __init__(self, mode, x, y, z: str):
        self.mode = mode
        
        x1, x2 = [int(a) for a in x.split("..")]
        y1, y2 = [int(a) for a in y.split("..")]
        z1, z2 = [int(a) for a in z.split("..")]

        self.p1 = Point(x1, y1, z1)
        self.p2 = Point(x2, y2, z2)

    def get_contained_points(self) -> Generator[Point, None, None]:
        for x in range(self.p1.x, self.p2.x+1):
            for y in range(self.p1.y, self.p2.y+1):
                for z in range(self.p1.z, self.p2.z+1):
                    yield Point(x, y, z)


def parse(instr: str) -> List[Shape]:
    o = []
    for line in instr.strip().splitlines():
        sp = line.split(" ")
        x, y, z = [x.split("=")[-1] for x in sp[-1].split(",")]
        o.append(Shape(sp[0], x, y, z))
    return o


def is_point_out_of_bounds(p: Point) -> bool:
    return not (-50 <= p.x <= 50 and -50 <= p.y <= 50 and -50 <= p.z <= 50)


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        shapes = parse(instr)
        points = {}
        for shape in shapes:
            
            if is_point_out_of_bounds(shape.p1) and is_point_out_of_bounds(shape.p2):
                continue

            for p in shape.get_contained_points():
                
                if is_point_out_of_bounds(p):
                    continue

                if (p in points) and (shape.mode == MODE_OFF):
                    del points[p]
                elif (p not in points) and (shape.mode == MODE_ON):
                    points[p] = True
                    
        return len(points)

    @staticmethod
    def two(instr: str) -> Any:
        raise NotImplementedError
