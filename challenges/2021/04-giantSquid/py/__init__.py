from typing import List, Tuple, Optional
from aocpy import BaseChallenge
from dataclasses import dataclass


BOARD_EDGE = 5  # assuming our boards are square, how long is one edge of the board?

WINNING_SEQUENCES = (
    (0, 1, 2, 3, 4),
    (5, 6, 7, 8, 9),
    (10, 11, 12, 13, 14),
    (15, 16, 17, 18, 19),
    (20, 21, 22, 23, 24),
    (0, 5, 10, 15, 20),
    (1, 6, 11, 16, 21),
    (2, 7, 12, 17, 22),
    (3, 8, 13, 18, 23),
    (4, 9, 14, 19, 24),
)


@dataclass
class Point:
    value: int
    marked: bool


Board = List[Point]


def parse(instr: str) -> Tuple[List[int], List[Board]]:
    numbers, rawBoards = instr.strip().split("\n", 1)

    numbers = list(map(int, numbers.split(",")))
    rawBoards = rawBoards.strip().split("\n\n")

    boards = []
    for rb in rawBoards:
        boards.append(
            [Point(int(x), False) for x in rb.replace("\n", " ").split(" ") if x != ""]
        )

    return numbers, boards


def check_for_winning_boards(boards: List[Board]) -> List[int]:
    # returns a list of indexes in `boards` that have won.

    winning_boards = []

    for i, board in enumerate(boards):
        for sequence in WINNING_SEQUENCES:
            has_sequence = True
            for n in sequence:
                has_sequence = has_sequence and board[n].marked

            if has_sequence:
                winning_boards.append(i)
                break

    return winning_boards


def calculate_board_score(board: Board, last_called_number: int) -> int:
    sigma = sum([n.value for n in board if not n.marked])
    return sigma * last_called_number


def play_round(boards: List[Board], number: int) -> List[Board]:
    # plays a round of bingo, removes winning boards from `boards` and returns them.

    for board in boards:
        for board_number in board:
            if number == board_number.value:
                board_number.marked = True
                break  # assume each number only exists once in each board

    winning_boards = check_for_winning_boards(boards)
    o = []
    for board_number in reversed(sorted(winning_boards)):
        o.append(boards.pop(board_number))
    return o


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        numbers, boards = parse(instr)

        for number in numbers:

            winning_boards = play_round(boards, number)
            if len(winning_boards) != 0:
                assert len(winning_boards) == 1
                return calculate_board_score(winning_boards[0], number)

        return -1

    @staticmethod
    def two(instr: str) -> int:
        numbers, boards = parse(instr)

        winners = []

        for number in numbers:
            winners += play_round(boards, number)

            if len(boards) == 0:
                break

        return calculate_board_score(winners[-1], number)
