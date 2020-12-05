import re

from common import *

def partOne(instr:str) -> int:
    input_string = parse(instr)

    class Password:
        plaintext: str
        target_letter: str
        min_repeats: int
        max_repeats: int

        def __init__(self, plaintext:str, target_letter:str, min_repeats:int, max_repeats:int) -> None:
            self.plaintext = plaintext
            self.target_letter = target_letter
            self.min_repeats = min_repeats
            self.max_repeats = max_repeats

    parser_regex = r"(\d+)-(\d+) ([a-z]): (.+)"

    passwords = []

    for line in input_string:
        m = re.match(parser_regex, line)
        passwords.append(Password(m.group(4), m.group(3), int(m.group(1)), int(m.group(2))))

    num_valid_passwords = 0

    for password in passwords:
        target_letter_count = 0
        for char in password.plaintext:
            if char == password.target_letter:
                target_letter_count += 1

        if password.min_repeats <= target_letter_count <= password.max_repeats:
            num_valid_passwords += 1
    
    return num_valid_passwords
