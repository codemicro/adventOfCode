import itertools
from typing import List
from aocpy import BaseChallenge
from dataclasses import dataclass


DIGITS = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]

POSSIBLE_WIRINGS = list(itertools.permutations("abcdefg", 7))


@dataclass
class Display:
    samples: List[str]
    outputs: List[str]


def parse(instr: str) -> List[Display]:
    def sort_string(s: str) -> str:
        return "".join(sorted(s))

    o = []
    for line in instr.strip().splitlines():
        samples, output = line.split(" | ")
        o.append(
            Display(
                [sort_string(x) for x in samples.split(" ")],
                [sort_string(x) for x in output.split(" ")],
            )
        )
    return o


def is_digit_valid(digit: str) -> bool:
    return digit in DIGITS


def translate_digit(mapping: str, input_digit: str) -> str:
    o = ""
    for char in input_digit:
        n = ord(char) - ord("a")
        o += mapping[n]
    return "".join(sorted(o))


def is_wiring_valid(samples: List[str], wiring: str) -> bool:
    for sample in samples:
        if not is_digit_valid(translate_digit(wiring, sample)):
            return False
    return True


def find_valid_wiring_from_samples(samples: List[str]) -> str:
    for wiring in POSSIBLE_WIRINGS:
        if is_wiring_valid(samples, wiring):
            return wiring
    raise ValueError("no valid wiring")


def get_display_output(display: Display) -> int:
    valid_wiring = find_valid_wiring_from_samples(display.samples)
    o = 0
    for digit in display.outputs:
        o *= 10
        translated = translate_digit(valid_wiring, digit)
        o += DIGITS.index(translated)
    return o


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        displays = parse(instr)
        sigma = 0
        for display in displays:
            for digit in display.outputs:
                ld = len(digit)
                if (
                    ld == len(DIGITS[1])
                    or ld == len(DIGITS[4])
                    or ld == len(DIGITS[7])
                    or ld == len(DIGITS[8])
                ):
                    sigma += 1
        return sigma

    @staticmethod
    def two(instr: str) -> int:
        displays = parse(instr)
        sigma = 0
        for display in displays:
            sigma += get_display_output(display)
        return sigma
