import re
from typing import Dict


rule_regex = re.compile(r"(.+) bags contain (.+).")
definition_regex = re.compile(
    r"(\d+) (.+) bags?"
)  # A definiton is the section of a rule that contains the conditions


target_colour = "shiny gold"


def parse(instr: str) -> Dict[str, Dict[str, int]]:
    inp = instr.strip().split("\n")

    rules = {}

    for rule in inp:
        rr = rule_regex.match(rule)
        container_bag = rr.group(1)
        rule_set = rr.group(2).split(", ")

        bag_rules = {}

        for definition in rule_set:
            rsr = definition_regex.match(definition)
            # if this is false, it probably means we've encountered something saying "no other bags"
            if rsr is not None:
                bag_rules[rsr.group(2)] = int(rsr.group(1))

        rules[container_bag] = bag_rules

    return rules
