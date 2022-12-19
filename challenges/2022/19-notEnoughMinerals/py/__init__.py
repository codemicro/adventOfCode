from typing import *
from aocpy import BaseChallenge, foldl
from dataclasses import dataclass
import re
from enum import Enum


class Material(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


MaterialTracker = Tuple[int, int, int, int]


@dataclass(init=False)
class Blueprint:
    number: int

    robots: Dict[Material, MaterialTracker]

    def __init__(self, number: int, ore_robot_cost: int, clay_robot_cost: int, obsidian_robot_cost_ore: int, obsidian_robot_cost_clay: int, geode_robot_cost_ore: int, geode_robot_cost_obsidian: int):
        self.number = number
    
        self.robots = {
            Material.ORE: (ore_robot_cost, 0, 0, 0),
            Material.CLAY: (clay_robot_cost, 0, 0, 0),
            Material.OBSIDIAN: (obsidian_robot_cost_ore, obsidian_robot_cost_clay, 0, 0),
            Material.GEODE: (geode_robot_cost_ore, 0, geode_robot_cost_obsidian, 0),
        }

    def iter_robots(self) -> Generator[Tuple[Material, MaterialTracker], None, None]:
        for key in self.robots:
            yield (key, self.robots[key])

    def __hash__(self) -> int:
        return hash(self.number)


parse_re = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.")


def parse(instr: str) -> List[Blueprint]:
    res: List[Blueprint] = []
    for line in instr.strip().splitlines():
        res.append(
            Blueprint(*map(int, parse_re.match(line).groups())),
        )
    return res


def calc_max_geodes(blueprint: Blueprint, max_time: int, materials: MaterialTracker, robots: MaterialTracker, robot_quota: MaterialTracker, minute: int, cannot_build: int) -> int:
    if minute == max_time + 1:
        return materials[Material.GEODE.value]

    try_build: int = 0
    for (robot_type, robot_materials) in blueprint.iter_robots():
        rtv = robot_type.value
        if cannot_build & (1 << rtv) != 0:
            continue

        if robot_type != Material.GEODE and robots[rtv] == robot_quota[rtv]:
            continue

        has_enough_materials = True
        for (required, available) in zip(robot_materials, materials):
            if required > available:
                has_enough_materials = False
                break

        if has_enough_materials:
            try_build = try_build | (1 << robot_type.value)

    materials = (
        materials[0] + robots[0],
        materials[1] + robots[1],
        materials[2] + robots[2],
        materials[3] + robots[3],
    )

    max_score = 0
    for i in range(5):
        if i == 4 and cannot_build | try_build != 0b1111:
            # always try not building anything
            sc = calc_max_geodes(blueprint, max_time, materials, robots, robot_quota, minute + 1, cannot_build | try_build)
        else:
            if try_build & (1 << i) == 0:
                continue

            robot_type = Material(i)
            robot_materials = blueprint.robots[robot_type]

            # subtract materials required to build this robot
            mc = (
                materials[0] - robot_materials[0],
                materials[1] - robot_materials[1],
                materials[2] - robot_materials[2],
                materials[3],
            )

            # update robot counts
            rc = tuple((robots[j] + (1 if i == j else 0) for j in range(4)))

            # recurse
            sc = calc_max_geodes(blueprint, max_time, mc, rc, robot_quota, minute + 1, 0)
        
        if sc is not None and sc > max_score:
            max_score = sc
        
    return max_score


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)

        quals: List[int] = []
        for bp in inp:
            robot_quota: Tuple[int] = tuple(max(x) for x in zip(*bp.robots.values()))
            quals.append(
                calc_max_geodes(bp, 24, (0,0,0,0), (1,0,0,0), robot_quota, 1, 0) * bp.number,
            )

        return sum(quals)

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)

        nums: List[int] = []
        for bp in inp[:min(3, len(inp))]:
            print(f"{bp.number=}", flush=True)
            robot_quota: Tuple[int] = tuple(max(x) for x in zip(*bp.robots.values()))
            nums.append(
                calc_max_geodes(bp, 32, (0,0,0,0), (1,0,0,0), robot_quota, 1, 0)
            )
            print(nums[-1], flush=True)

        return foldl(lambda x, y: x * y, nums, 1)
