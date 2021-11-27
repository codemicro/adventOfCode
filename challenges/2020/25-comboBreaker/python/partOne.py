from common import *


def single_transformation(v:int, subject_number:int=7) -> int:
    return (v * subject_number) % 20201227


def transform(loop_size:int, subject_number:int=7) -> int:
    v = 1
    for _ in range(loop_size):
        v = single_transformation(v, subject_number=subject_number)
    return v


def find_loop_size(target_pubkey:int) -> int:
    c = 0
    v = 1
    while True:
        c += 1
        v = single_transformation(v)
        if v == target_pubkey:
            return c


def partOne(instr: str) -> int:
    pubkey_one, pubkey_two = parse(instr)

    loop_size_one = find_loop_size(pubkey_one)
    loop_size_two = find_loop_size(pubkey_two)

    encryption_key = transform(loop_size_two, subject_number=pubkey_one)
    assert encryption_key == transform(loop_size_one, subject_number=pubkey_two), "encryption keys do not match"

    return encryption_key
