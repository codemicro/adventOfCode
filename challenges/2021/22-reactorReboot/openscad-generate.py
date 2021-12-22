import sys
from dataclasses import dataclass
from typing import List, Tuple, NamedTuple, Generator


# This script exists to generate OpenSCAD code to represent challenge inputs.


MODE_ON = "on"
MODE_OFF = "off"


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def to_list(self) -> List[int]:
        return [self.x, self.y, self.z]

def apply_point_shift(point: List[int], shift: Tuple[int, int, int]) -> List[int]:
    x, y, z = point
    xs, ys, zs = shift
    return [x+abs(xs), y+abs(ys), z+abs(zs)]

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

    def verticies(self) -> List[Point]:
        p1 = self.p1
        p2 = Point(self.p2.x + 1, self.p2.y + 1, self.p2.z + 1)
        return [
            p1,
            Point(p2.x, p1.y, p1.x),
            Point(p2.x, p2.y, p1.x),
            Point(p1.x, p2.y, p1.x),
            Point(p1.x, p1.y, p2.x),
            Point(p2.x, p1.y, p2.x),
            p2,
            Point(p1.x, p2.y, p2.x),
        ]

    def openscad(self) -> str:
        shift = self.p1.to_list()
        o = "cube("
        o += str(Point(self.p2.x+1-self.p1.x, self.p2.y+1-self.p1.y, self.p2.z+1-self.p1.z).to_list())
        o += ", center=false);"
        if shift[0] != 0 and shift[1] != 0 and shift[2] != 0:
            o = "translate(" + str(shift) + ") {\n" + o + "\n};"
        return o 


def parse(instr: str) -> List[Shape]:
    o = []
    for line in instr.strip().splitlines():
        sp = line.split(" ")
        x, y, z = [x.split("=")[-1] for x in sp[-1].split(",")]
        o.append(Shape(sp[0], x, y, z))
    return o

def is_point_out_of_bounds(p: Point) -> bool:
    return not (-50 <= p.x <= 50 and -50 <= p.y <= 50 and -50 <= p.z <= 50)

def main(part_one_only=False):
    shapes = parse(open("input.txt").read())

    current_program = shapes[0].openscad()
    for shape in shapes[1:]:

        if is_point_out_of_bounds(shape.p1) and is_point_out_of_bounds(shape.p2) and not part_one_only:
            continue

        function = ""
        if shape.mode == MODE_ON:
            function = "union"
        else:
            function = "difference"

        current_program = function + "() {\n" + current_program + "\n" + shape.openscad() + "\n};"

    print(current_program)

if __name__ == "__main__":
    x = False
    if len(sys.argv) > 1:
        x = bool(sys.argv[1])
    main(x)
