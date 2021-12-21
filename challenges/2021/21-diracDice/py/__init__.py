from typing import Any, List, Tuple
from aocpy import BaseChallenge


class DeterministicDie:
    num_rolls: int

    def __init__(self, sides: int = 100):
        self._sides = sides
        self._n = 0
        self.num_rolls = 0

    def next_number(self) -> int:
        self.num_rolls += 1
        self._n += 1
        if self._n > self._sides:
            self._n = 1
        return self._n

    def next_n_numbers(self, n: int) -> List[int]:
        o = []
        for _ in range(n):
            o.append(self.next_number())
        return o


Player = List[int]  # position, score
Players = Tuple[Player, Player]


def parse(instr: str) -> Players:
    o = []
    for line in instr.strip().splitlines():
        start_pos = int(line.split(": ")[-1])
        o.append([start_pos, 0])
    return tuple(o)


def get_next_position(current_position: int, steps: int) -> int:
    n = current_position + (steps % 10)
    return n if n <= 10 else n - 10


def move_player_forwards_by(p: Player, steps: int):
    p[0] = get_next_position(p[0], steps)
    p[1] = p[1] + p[0]


def get_player_score(p: Player) -> int:
    return p[1]


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> Any:
        players = parse(instr)
        die = DeterministicDie()
        while True:
            game_finished = False

            for player in players:
                forward_steps = sum(die.next_n_numbers(3))
                move_player_forwards_by(player, forward_steps)
                if get_player_score(player) >= 1000:
                    game_finished = True
                    break

            if game_finished:
                break

        scores = list(sorted([get_player_score(p) for p in players]))
        return scores[0] * die.num_rolls

    @staticmethod
    def two(instr: str) -> int:
        return NotImplementedError
