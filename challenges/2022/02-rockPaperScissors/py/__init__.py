from typing import *
from aocpy import BaseChallenge


Match = List[str]

ROCK = "A"
PAPER = "B"
SCISSORS = "C"

LOSE = "X"
DRAW = "Y"
WIN = "Z"

SCORES = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
    WIN: 6,
    LOSE: 0,
    DRAW: 3,
}


magic_beans = [SCISSORS, ROCK, PAPER, SCISSORS, ROCK]

outcome_offsets = {
    WIN: 1,
    LOSE: -1,
    DRAW: 0,
}


def parse(instr: str) -> List[Match]:
    return [x.split(" ") for x in instr.strip().splitlines()]


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        inp = parse(instr)

        for i, m in enumerate(inp):
            m[1] = m[1].replace("X", ROCK).replace("Y", PAPER).replace("Z", SCISSORS)
            inp[i] = m

        score = 0
        for m in inp:
            score += SCORES[m[1]]

            if m[0] == m[1]:
                score += SCORES[DRAW]
            else:
                opponent = magic_beans.index(m[1], 1)
                ours = magic_beans.index(m[0], opponent-1, opponent+2)
                
                if opponent - ours == outcome_offsets[WIN]:
                    score += SCORES[WIN]

        return score

    @staticmethod
    def two(instr: str) -> int:
        inp = parse(instr)

        score = 0
        for m in inp:
            score += SCORES[m[1]]
            our_move = magic_beans[magic_beans.index(m[0], 1) + outcome_offsets[m[1]]]
            score += SCORES[our_move]

        return score
