from typing import *
from aocpy import BaseChallenge
import json
from functools import cmp_to_key


_Pair = Union[int, List['_Pair']]
Pair = Tuple[_Pair, _Pair]

def parse(instr: str) -> List[Pair]:
    res = []

    for raw_pair in instr.strip().split("\n\n"):
        a, b = raw_pair.splitlines()
        res.append((
            json.loads(a),
            json.loads(b),
        ))

    return res


def is_pair_well_ordered(pair: Pair) -> Optional[bool]:
    (a, b) = pair
    type_a, type_b = type(a), type(b)

    if type_a == int and type_b == list:
        return is_pair_well_ordered(([a], b))
    
    elif type_a == list and type_b == int:
        return is_pair_well_ordered((a, [b]))

    elif type_a == int and type_b == int:
        if a == b:
            return None
        return a < b
        
    elif type_a == list and type_b == list:
    
        for x in zip(a, b):
            y = is_pair_well_ordered(x)
            if y is not None:
                return y

        la, lb = len(a), len(b)

        if la == lb:
            return None
        return la < lb
    
    raise ValueError(f"impossible combiation of types ({type_a} and {type_b})")


@cmp_to_key
def is_well_ordered(a, b: Any) -> int:
    x = is_pair_well_ordered((a, b))
    if x is None:
        return 0
    return 1 if x else -1


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)
        sigma = 0
        for i, pair in enumerate(inp):
            if is_pair_well_ordered(pair):
                sigma += i + 1
        return sigma

    @staticmethod
    def two(instr: str) -> int:
        inp = [[[2]], [[6]]]
        for (a, b) in parse(instr):
            inp.append(a)
            inp.append(b)

        inp.sort(key=is_well_ordered, reverse=True)

        return (inp.index([[2]]) + 1) * (inp.index([[6]]) + 1)