from dataclasses import dataclass
from typing import Any, List, SupportsIndex
from aocpy import BaseChallenge


class Consumer:
    def __init__(self, instr: str):
        self.input = instr
        self.pointer = 0

    def get(self) -> str:
        return self.get_n(1)

    def get_n(self, n) -> str:
        self.pointer += n
        if self.pointer > len(self.input):
            raise IndexError("index out of bounds")
        return self.input[self.pointer-n:self.pointer]

    def finished(self) -> bool:
        return len(self.input) == self.pointer

@dataclass
class Packet:
    version: int
    type_indicator: int
    content: Any

def hex_to_binary_string(n: str) -> str:
    o = ""
    for char in n:
        o += bin(int(char, base=16))[2:].zfill(4)
    return o

def from_binary_string(x: str) -> int:
    return int(x, base=2)

def decode_all(input_stream: Consumer) -> List[Packet]:
    o = []
    while True:
        try:
            o.append(decode_one(input_stream))
        except IndexError:
            break
    return o

def decode_one(input_stream: Consumer) -> Packet:
    version = from_binary_string(input_stream.get_n(3))
    packet_type = from_binary_string(input_stream.get_n(3))

    if packet_type == 4:
        literal_number = 0
        while True:
            continue_bit = from_binary_string(input_stream.get())
            literal_number = (literal_number << 4) | from_binary_string(input_stream.get_n(4))
            if continue_bit == 0:
                break
        return Packet(version, packet_type, literal_number)
    else:
        length_type = from_binary_string(input_stream.get())
        if length_type == 0:
            # 15 bit subpackt length indicator
            run_length = from_binary_string(input_stream.get_n(15))
            content = decode_all(Consumer(input_stream.get_n(run_length)))
            return Packet(version, packet_type, content)
        else:
            # 11 bit subpacket count
            subpacket_count = from_binary_string(input_stream.get_n(11))
            content = []
            for _ in range(subpacket_count):
                content.append(decode_one(input_stream))
            return Packet(version, packet_type, content)


def parse(instr: str) -> List[Packet]:
    return decode_all(Consumer(hex_to_binary_string(instr.strip())))


def sum_version_numbers(packets: List[Packet]) -> int:
    sigma = 0 
    for packet in packets:
        sigma += packet.version
        if type(packet.content) == list:
            sigma += sum_version_numbers(packet.content)
    return sigma


def interpet_packet(packet: Packet) -> int:
    if packet.type_indicator == 0:
        # sum packet
        sigma = 0
        for subpacket in packet.content:
            sigma += interpet_packet(subpacket)
        return sigma
    elif packet.type_indicator == 1:
        # product packet
        product = 1
        for subpacket in packet.content:
            product *= interpet_packet(subpacket)
        return product
    elif packet.type_indicator == 2:
        # min packet
        vals = []
        for subpacket in packet.content:
            vals.append(interpet_packet(subpacket))
        return min(vals)
    elif packet.type_indicator == 3:
        # max packet
        vals = []
        for subpacket in packet.content:
            vals.append(interpet_packet(subpacket))
        return max(vals)
    elif packet.type_indicator == 4:
        return packet.content
    elif packet.type_indicator == 5:
        # greater than packet
        first = interpet_packet(packet.content[0])
        second = interpet_packet(packet.content[1])
        return 1 if first > second else 0
    elif packet.type_indicator == 6:
        # less than packet
        first = interpet_packet(packet.content[0])
        second = interpet_packet(packet.content[1])
        return 1 if first < second else 0
    elif packet.type_indicator == 7:
        # equal to packet
        first = interpet_packet(packet.content[0])
        second = interpet_packet(packet.content[1])
        return 1 if first == second else 0
    else:
        raise ValueError(f"unknown packet type {packet.type_indicator}")


class Challenge(BaseChallenge):

    @staticmethod
    def one(instr: str) -> int:
        packets = parse(instr)
        return sum_version_numbers(packets)

    @staticmethod
    def two(instr: str) -> int:
        packets = parse(instr)
        return interpet_packet(packets[0])
