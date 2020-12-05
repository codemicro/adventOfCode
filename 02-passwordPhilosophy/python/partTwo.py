import re

from common import *

def partTwo(instr:str) -> int:
    input_string = parse(instr)

    class Password:
        plaintext: str
        target_letter: str
        position_one: int
        position_two: int

        def __init__(self, plaintext:str, target_letter:str, position_one:int, position_two:int) -> None:
            self.plaintext = plaintext
            self.target_letter = target_letter
            self.position_one = position_one - 1  # No concept of index zero... eurgh
            self.position_two = position_two - 1

    parser_regex = r"(\d+)-(\d+) ([a-z]): (.+)"

    passwords = []

    for line in input_string:
        m = re.match(parser_regex, line)
        passwords.append(Password(m.group(4), m.group(3), int(m.group(1)), int(m.group(2))))

    num_valid_passwords = 0

    for password in passwords:
        position_one_matches = password.plaintext[password.position_one] == password.target_letter
        position_two_matches = password.plaintext[password.position_two] == password.target_letter

        if position_one_matches ^ position_two_matches:
            num_valid_passwords += 1        
    
    return num_valid_passwords
