from common import *
import re


def recurse_replace(instr: str, old: str, new: str, limit: int, n: int = 0) -> str:
    # I *think* this is tail recursive?
    if n + 1 == limit:
        return instr
    return recurse_replace(instr.replace(old, new), old, new, limit, n=n + 1)


def partTwo(instr: str) -> int:

    # patch input
    instr = instr.replace(
        "8: 42", "8: 42 | 42 8"
    )  # the new rule 8 can be expressed as 42 | 42+
    instr = instr.replace("11: 42 31", "11: 42 31 | 42 11 31")

    rules, messages = parse(instr)

    # Since we have sections of our ruleset, we have markers in the regex returned by `make_ruleset_regex`
    # that denote where we need to insert a copy of the rule 11 regular expression (which also happens to
    # have one of those markers in it)

    rr = make_ruleset_regex(rules)
    eleven_regex = generate_rule_regex(rules, 11)
    for _ in range(10):
        rr = rr.replace(replace_marker, eleven_regex)

    # run as usual
    rule_regex = re.compile(rr)
    return run(messages, rule_regex)
