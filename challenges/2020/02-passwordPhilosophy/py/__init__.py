import re
from typing import List
from aocpy import BaseChallenge


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        input_string = parse(instr)

        class Password:
            plaintext: str
            target_letter: str
            min_repeats: int
            max_repeats: int

            def __init__(
                self, plaintext: str, target_letter: str, min_repeats: int, max_repeats: int
            ) -> None:
                self.plaintext = plaintext
                self.target_letter = target_letter
                self.min_repeats = min_repeats
                self.max_repeats = max_repeats

        parser_regex = r"(\d+)-(\d+) ([a-z]): (.+)"

        passwords = []

        for line in input_string:
            m = re.match(parser_regex, line)
            passwords.append(
                Password(m.group(4), m.group(3), int(m.group(1)), int(m.group(2)))
            )

        num_valid_passwords = 0

        for password in passwords:
            target_letter_count = 0
            for char in password.plaintext:
                if char == password.target_letter:
                    target_letter_count += 1

            if password.min_repeats <= target_letter_count <= password.max_repeats:
                num_valid_passwords += 1

        return num_valid_passwords

    @staticmethod
    def two(instr: str) -> int:
        input_string = parse(instr)

        class Password:
            plaintext: str
            target_letter: str
            position_one: int
            position_two: int

            def __init__(
                self,
                plaintext: str,
                target_letter: str,
                position_one: int,
                position_two: int,
            ) -> None:
                self.plaintext = plaintext
                self.target_letter = target_letter
                self.position_one = position_one - 1  # No concept of index zero... eurgh
                self.position_two = position_two - 1

        parser_regex = r"(\d+)-(\d+) ([a-z]): (.+)"

        passwords = []

        for line in input_string:
            m = re.match(parser_regex, line)
            passwords.append(
                Password(m.group(4), m.group(3), int(m.group(1)), int(m.group(2)))
            )

        num_valid_passwords = 0

        for password in passwords:
            position_one_matches = (
                password.plaintext[password.position_one] == password.target_letter
            )
            position_two_matches = (
                password.plaintext[password.position_two] == password.target_letter
            )

            if position_one_matches ^ position_two_matches:
                num_valid_passwords += 1

        return num_valid_passwords


def parse(instr: str) -> List:
    return instr.strip().split("\n")