from typing import List, Tuple
from aocpy import BaseChallenge


def parse(instr: str) -> Tuple[List[int], int]:
    # parse returns a list of integers and the original length of the first of
    # those integers in the binary representation in the input.

    y = instr.strip().splitlines()
    return [int(x, base=2) for x in y], len(y[0])


def get_bit(number: int, n: int) -> int:
    # get_bit returns a given bit from the binary representation of `number`.
    #
    # In the number 111001011110, n=4 would refer to this bit:
    #                      ^
    return (number >> n) & 0b1


def analyse_bits(numbers: List[int], n: int) -> Tuple[int, int]:
    # analyse_bits returns a tuple containing the most common bit (either 1 or
    # 0) and the least common bit (either 1 or 0) in position `n` of each
    # number in `numbers`.
    #
    # If the most common bit and least common bit occur the same amount of
    # times, both return values are -1.
    #
    # Returns: most common bit, least common bit

    zeros = 0
    ones = 0

    for number in numbers:
        sel = get_bit(number, n)
        if sel == 0:
            zeros += 1
        elif sel == 1:
            ones += 1

    if zeros > ones:
        return 0, 1
    elif ones > zeros:
        return 1, 0
    return -1, -1


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        numbers, bit_length = parse(instr)

        gamma = ""
        epsilon = ""

        for bit_number in reversed(range(bit_length)):

            most_common, least_common = analyse_bits(numbers, bit_number)
            gamma += str(most_common)
            epsilon += str(least_common)

        return int(gamma, 2) * int(epsilon, 2)

    @staticmethod
    def two(instr: str) -> int:
        numbers, bit_length = parse(instr)

        def find(inp: List[int], use_most_common: bool, n: int = bit_length - 1) -> int:
            # find implements the bit criteria-based filtering as defined in
            # AoC 2021 day 3 part 2. If `use_most_common` is True, the bit
            # criteria for the oxygen generator rating is used, else, the bit
            # criteria for the CO2 scrubber rating is used.

            if len(inp) == 1:
                return inp[0]

            most_common, least_common = analyse_bits(inp, n)

            target = None
            if most_common == -1 or least_common == -1:
                target = 1 if use_most_common else 0
            else:
                target = most_common if use_most_common else least_common

            # oooo, accidental tail recursion!
            return find(
                list(
                    filter(
                        lambda x: get_bit(x, n) == target,
                        inp,
                    )
                ),
                use_most_common,
                n - 1,
            )

        o2_rating = find(numbers, True)
        co2_rating = find(numbers, False)

        return o2_rating * co2_rating
