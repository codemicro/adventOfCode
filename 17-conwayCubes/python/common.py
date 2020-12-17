from typing import List, Tuple
import math


active = "#"
inactive = "."


class Matrix3D:
    master_array: List[List[List]]
    x_zero: int
    y_zero: int
    z_zero: int

    def __init__(self, x, y, z, default_value=None):
        self.master_array = [[[default_value for _ in range(x)] for _ in range(y)] for _ in range(z)]
        self.x_zero = math.floor(len(self.master_array[0][0]) / 2)
        self.y_zero = math.floor(len(self.master_array[0]) / 2)
        self.z_zero = math.floor(len(self.master_array) / 2)

    def translate(self, x:int, y:int, z:int) -> Tuple[int, int, int]:
        x += self.x_zero
        y += self.y_zero
        z += self.z_zero
        return x, y, z

    def __str__(self) -> str:
        return str(self.master_array)

    def __getitem__(self, location_tuple:Tuple[int, int, int]):
        x, y, z = location_tuple

        if x < 0 or y < 0 or z < 0:
            raise IndexError("list index out of range")

        return self.master_array[z][y][x]

    def __setitem__(self, location_tuple:Tuple[int, int, int], value):
        x, y, z = location_tuple

        if x < 0 or y < 0 or z < 0:
            raise IndexError("list index out of range")

        self.master_array[z][y][x] = value


def parse(instr: str) -> int:

    return 0
