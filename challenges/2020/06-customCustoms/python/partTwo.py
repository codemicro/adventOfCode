from common import *
from typing import Dict


def check_char(aq: Dict[int, List[str]], char: str) -> bool:
    is_in_all = True
    for key in aq:
        val = aq[key]
        if char not in val:
            is_in_all = False
            break
    return is_in_all


class Group:
    questions: List[str]
    num_pax: int

    def __init__(self, instr: str) -> None:
        individual_pax = instr.split("\n")
        self.num_pax = len(individual_pax)
        self.questions = []

        pax_questions = {}
        for i, pax in enumerate(individual_pax):
            pax_questions[i] = [char for char in pax]

        for key in pax_questions:
            val = pax_questions[key]
            for char in val:
                if check_char(pax_questions, char):
                    if char not in self.questions:
                        self.questions.append(char)


def partTwo(instr: str) -> int:
    groups = [Group(x) for x in parse(instr)]

    question_total = 0

    for group in groups:
        question_total += len(group.questions)

    return question_total
