from typing import *
from aocpy import BaseChallenge


SNAFU_DIGITS = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

REGULAR_DIGITS = {SNAFU_DIGITS[k]: k for k in SNAFU_DIGITS}


def parse(instr: str) -> List[str]:
    return instr.strip().splitlines()


def decode_snafu(snafu: str) -> int:
    acc = 0
    for i, char in enumerate(reversed(snafu)):
        acc += SNAFU_DIGITS[char] * pow(5, i)
    return acc


def encode_snafu(n: int) -> str:
    acc = []
    while n != 0:
        rem = n % 5
        acc.append(rem)
        n = n // 5

    for i in range(len(acc)):
        if acc[i] > 2:
            acc[i] = acc[i] - 5
            if i + 1 < len(acc):
                acc[i + 1] = acc[i + 1] + 1
            else:
                acc.append(1)

    return "".join(map(lambda x: REGULAR_DIGITS[x], reversed(acc)))


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> str:
        return encode_snafu(sum(map(decode_snafu, parse(instr))))

    @staticmethod
    def two(instr: str) -> str:
        return "Merry Christmas!"
