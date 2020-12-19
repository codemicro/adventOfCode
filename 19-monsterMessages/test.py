import re
from typing import Dict
import time

char_regex = re.compile(r"^\"([a-z])\"$") # group 1 contains interesting information
or_rule_regex = re.compile(r"^((\d+ ?)+) \| ((\d+ ?)+)$") # group 1 and 3 contain interesting info
single_rule_regex = re.compile(r"^((\d+ ?)+)$") # group 0 and 1 both contain the same interesting information

rules = {
    0: "4 1 5",
    1: "2 3 | 3 2",
    2: "4 4 | 5 5",
    3: "4 5 | 5 4",
    4: "\"a\"",
    5: "\"b\"",
}

def generate_compound_rule(ruleset:Dict[int, str], compound:str) -> str:
    o = ""
    for x in [int(a) for a in compound.split(" ")]:
        o += generate_rule(ruleset, rule=x)
    return o


memo = {}


def generate_rule(ruleset:Dict[int, str], rule:int=0) -> str:

    if rule in memo:
        return memo[rule]

    output = ""

    rule_content = ruleset[rule]

    r = char_regex.match(rule_content)
    if r:
        # is a single character
        return r.group(1)    
    
    # if we get here, that means there are multiple options for the rule
    # hence we need to open a new set of brackets
    output += "("

    r = or_rule_regex.match(rule_content)
    if r:
        # rule is an OR rule
        output += generate_compound_rule(ruleset, r.group(1))
        output += "|"
        output += generate_compound_rule(ruleset, r.group(3))
    
    r = single_rule_regex.match(rule_content)
    if r:
        # rule is a simple sequence rule
        output += generate_compound_rule(ruleset, r.group(1))

    # close original set of brackets
    output += ")"

    memo[rule] = output

    return output


rules, _ = open("input.txt").read().strip().split("\n\n")

rules_dict = {}
for x in rules.split("\n"):
    num, definition = x.split(":")
    rules_dict[int(num.strip())] = definition.strip()

res = generate_rule(rules_dict)
print("^" + res + "$")
