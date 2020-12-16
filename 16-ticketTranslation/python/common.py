from typing import List, Tuple

class Rule:
    name: str
    ranges: Tuple[int, ...]

    def __init__(self, instr:str) -> None:
        # arrival location: 26-482 or 504-959
        field, conditions = instr.strip().split(": ")
        self.name = field
        ranges = conditions.split("or")
        self.ranges = tuple([int(x) for x in ranges[0].strip().split("-")] + [int(x) for x in ranges[1].strip().split("-")])

class Ticket:
    fields: Tuple[int]

    def __init__(self, instr:str) -> None:
        self.fields = tuple([int(x) for x in instr.strip().split(",")])

def parse(instr: str) -> Tuple[List[Rule], Ticket, List[Ticket]]:

    raw_rules, raw_my_ticket, raw_other_tickets = instr.strip().split("\n\n")

    rules = [Rule(x) for x in raw_rules.split("\n")]

    my_ticket = Ticket(raw_my_ticket.split("\n")[-1])

    other_tickets = [Ticket(x) for x in raw_other_tickets.strip("nearby tickets:\n").split("\n")]

    return rules, my_ticket, other_tickets

def test_value(value:int, condition:Tuple[int, ...]) -> bool:
    return condition[0] <= value <= condition[1] or condition[2] <= value <= condition[3]

def find_invalid(rules:List[Rule], tickets:List[Ticket]) -> Tuple[List[int], List[int]]:
    # returns invalid values and indexes of invalid tickets

    invalid_values = []
    invalid_indexes = []

    for i, ticket in enumerate(tickets):
        for field in ticket.fields:
            field_is_valid = False
            for rule in rules:
                if test_value(field, rule.ranges):
                    field_is_valid = True
            if not field_is_valid:
                invalid_values.append(field)
                invalid_indexes.append(i)

    return invalid_values, invalid_indexes