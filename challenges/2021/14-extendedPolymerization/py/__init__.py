import math
from typing import Tuple, List, Dict
from aocpy import BaseChallenge

Rule = Tuple[str, str]
Pairs = Dict[str, int]


def parse(instr: str) -> Tuple[str, List[Rule]]:
    seq, rawRules = instr.strip().split("\n\n")
    return seq, [tuple(x.split(" -> ")) for x in rawRules.splitlines()]


def make_pair_dict(seq: str) -> Pairs:
    o = {}
    for i in range(len(seq) - 1):
        s = seq[i] + seq[i + 1]
        o[s] = o.get(s, 0) + 1
    return o


def apply_rules(pairs: Pairs, rules: List[Rule]) -> Pairs:
    deltas = {}

    for rule in rules:
        rule_part_a = rule[0][0] + rule[1]
        rule_part_b = rule[1] + rule[0][1]

        if rule[0] in pairs:
            count = pairs[rule[0]]
            deltas[rule[0]] = deltas.get(rule[0], 0) - count
            deltas[rule_part_a] = deltas.get(rule_part_a, 0) + count
            deltas[rule_part_b] = deltas.get(rule_part_b, 0) + count

    for key in deltas:
        new = pairs.get(key, 0) + deltas[key]
        pairs[key] = 0 if new < 0 else new

    return pairs


def count_letters(pairs: Pairs) -> Dict[str, int]:
    o = {}
    for pair in pairs:
        n = pairs[pair]
        o[pair[0]] = o.get(pair[0], 0) + n
        o[pair[1]] = o.get(pair[1], 0) + n

    for key in o:
        o[key] = math.ceil(o[key] / 2)

    return o


class Challenge(BaseChallenge):
    @staticmethod
    def core(instr: str, n: int) -> int:
        sequence, rules = parse(instr)
        sequence_pairs = make_pair_dict(sequence)
        for _ in range(n):
            sequence_pairs = apply_rules(sequence_pairs, rules)
        vals = count_letters(sequence_pairs).values()
        return max(vals) - min(vals)

    @staticmethod
    def one(instr: str) -> int:
        return Challenge.core(instr, 10)

    @staticmethod
    def two(instr: str) -> int:
        return Challenge.core(instr, 40)
