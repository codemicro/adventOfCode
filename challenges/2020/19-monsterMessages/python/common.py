from typing import Dict, List, Tuple
import re


char_regex = re.compile(r"^\"([a-z])\"$")  # group 1 contains interesting information
or_rule_regex = re.compile(
    r"^((\d+ ?)+) \| ((\d+ ?)+)$"
)  # group 1 and 3 contain interesting info
single_rule_regex = re.compile(
    r"^((\d+ ?)+)$"
)  # group 0 and 1 both contain the same interesting information


replace_marker = "!!!REPLACETHISMARKER!!!"


def generate_compound_rule_regex(
    ruleset: Dict[int, str], compound: str, current: int
) -> str:

    # Used when you have a rule that looks like `125: 116 33 | 131 113`
    # compound should be a sequence like `116 33`
    # current should be the current rule number

    o = ""
    for x in [int(a) for a in compound.split(" ")]:
        if x == current:
            if x == 8:
                o += generate_rule_regex(ruleset, 42)
                o += "+"
            else:
                o += replace_marker
        else:
            o += generate_rule_regex(ruleset, x)

    return o


def generate_rule_regex(ruleset: Dict[int, str], rule: int) -> str:

    # Rule is the integer number of the rule to generate a regular expression for
    # Said integer should correspond to a key-value pair in the ruleset

    rule_content = ruleset[rule]

    r = char_regex.match(rule_content)
    if r:
        # is a single character
        # `116: "a"`
        return r.group(1)

    # if we get here, that means there are multiple options for the rule
    # hence we need to open a new set of brackets
    output = "("

    r = or_rule_regex.match(rule_content)
    if r:
        # rule is an OR rule
        # `83: 26 131 | 47 116`
        output += generate_compound_rule_regex(ruleset, r.group(1), rule)
        output += "|"
        output += generate_compound_rule_regex(ruleset, r.group(3), rule)

    r = single_rule_regex.match(rule_content)
    if r:
        # rule is a simple sequence rule
        # `92: 67 131`
        output += generate_compound_rule_regex(ruleset, r.group(1), rule)

    # close original set of brackets
    output += ")"

    return output


def make_ruleset_regex(ruleset: Dict[int, str]) -> str:
    return "^" + generate_rule_regex(ruleset, 0) + "$"


def run(messages: List[str], regex: re.Pattern) -> int:
    valid_inputs = 0
    for i, message in enumerate(messages):
        if regex.match(message):
            valid_inputs += 1
    return valid_inputs


def parse(instr: str) -> Tuple[Dict[int, str], List[str]]:

    rules, messages = instr.strip().split("\n\n")

    rule_dict = {}
    for x in rules.split("\n"):
        num, definition = x.split(":")
        rule_dict[int(num.strip())] = definition.strip()

    messages = messages.strip().split("\n")

    return rule_dict, messages
