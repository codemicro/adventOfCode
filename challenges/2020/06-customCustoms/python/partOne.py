from common import *


class Group:
    questions: List[str]
    num_pax: int

    def __init__(self, instr: str) -> None:
        individual_pax = instr.split("\n")
        self.num_pax = len(individual_pax)

        self.questions = []

        for pax in individual_pax:
            for char in pax:
                if char not in self.questions:
                    self.questions.append(char)


def partOne(instr: str) -> int:
    groups = [Group(x) for x in parse(instr)]

    question_total = 0

    for group in groups:
        question_total += len(group.questions)

    return question_total
