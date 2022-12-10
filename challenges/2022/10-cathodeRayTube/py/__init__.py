from typing import *
from aocpy import BaseChallenge

Instruction = Tuple[str, Optional[int]]

def parse(instr: str) -> List[Instruction]:
    res: List[Instruction] = []
    for line in instr.strip().splitlines():
        parts = line.split(" ")
        if len(parts) == 1:
            res.append((parts[0], None))
        elif len(parts) == 2:
            res.append((parts[0], int(parts[1])))
        else:
            raise ValueError(f"unexpected instruction length {len(parts)} for {line=}")
    return res


class MachineOne:
    ticks: int
    acc: int
    vals: List[int]

    def __init__(self):
        self.ticks = 0
        self.acc = 1
        self.vals = []

    def tick(self):
        self.ticks += 1

    def check_acc(self):
        tm = self.ticks % 40
        if tm == 20:
            self.vals.append(self.ticks * self.acc)

    def execute(self, ins: Instruction):
        (opcode, operand) = ins
        if opcode == "noop":
            self.tick()
            self.check_acc()
        elif opcode == "addx":
            self.tick()
            self.check_acc()
            self.tick()
            self.check_acc()
            self.acc += operand


class MachineTwo(MachineOne):
    output: str

    def __init__(self):
        super().__init__()
        self.output = ""

    def check_acc(self):
        tm = self.ticks % 40
        if tm == 0:
            self.output += "\n"

        if tm == 20:
            self.vals.append(self.ticks * self.acc)

        if self.acc - 1 <= tm <= self.acc + 1:
            self.output += "█"
        else:
            self.output += " "
    
    def execute(self, ins: Instruction):
        (opcode, operand) = ins
        if opcode == "noop":
            self.check_acc()
            self.tick()
        elif opcode == "addx":
            self.check_acc()
            self.tick()
            self.check_acc()
            self.tick()
            self.acc += operand


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)

        machine = MachineOne()
        for ins in inp:
            machine.execute(ins)
            
        return sum(machine.vals)

    @staticmethod
    def two(instr: str):
        inp = parse(instr)

        machine = MachineTwo()
        for ins in inp:
            machine.execute(ins)
            
        return "\n" + machine.output.strip()
