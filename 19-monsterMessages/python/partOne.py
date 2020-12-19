from common import *
import re


def partOne(instr: str) -> int:
    rules, messages = parse(instr)
    rule_regex = re.compile(make_ruleset_regex(rules))
    return run(messages, rule_regex)
