from common import *
from pprint import pprint


def partTwo(instr: str) -> int:
    rules, my_ticket, tickets = parse(instr)

    # purge bad indexes
    _, invalid_indexes = find_invalid(rules, tickets)
    invalid_indexes = list(reversed(sorted(invalid_indexes)))

    for idx in invalid_indexes:
        tickets.pop(idx)
    
    ticket_length = len(tickets[0].fields)
    num_tickets = len(tickets)
    num_rules = len(rules)

    candidates = {rule.name: set() for rule in rules}

    for col in range(ticket_length):
        values = [ticket.fields[col] for ticket in tickets]

        for rule_idx, rule in enumerate(rules):
            complete_match = True
            for v in values:
                if not test_value(v, rule.ranges):
                    complete_match = False
                    break

            if complete_match:
                candidates[rule.name].add(col)

    parameter_indexes = {}
    removed = set()

    product = 1

    for col in range(ticket_length):
        for name in candidates:
            candidates_set = candidates[name] - removed

            if len(candidates_set) == 1:
                idx = candidates_set.pop()
                parameter_indexes[name] = idx
                removed.add(idx)

    product = 1
    for param in parameter_indexes:
        if "departure" in param:
            product *= my_ticket.fields[parameter_indexes[param]]

    return product
