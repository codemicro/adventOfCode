import re

from common import *

def partOne(instr:str) -> int:
    input_list = parse(instr)

    test_cases = [
        # Regex to match expression, bool if can be skipped
        [r"byr:([^ ]+)", False],
        [r"iyr:([^ ]+)", False],
        [r"eyr:([^ ]+)", False],
        [r"hgt:([^ ]+)", False],
        [r"hcl:([^ ]+)", False],
        [r"ecl:([^ ]+)", False],
        [r"pid:([^ ]+)", False],
        [r"cid:([^ ]+)", True]
    ]

    valid_passports = 0

    for passport in input_list:

        results = []
        for tc in test_cases:
            results.append([re.search(tc[0], passport) is not None, tc[1]])

        valid = True
        for r in results:
            if not (r[0] or r[1]):
                valid = False
                break

        valid_passports += 1 if valid else 0

    return valid_passports
