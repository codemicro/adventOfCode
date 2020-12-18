import common
import matplotlib.pyplot as plt
from typing import List


def make_graph(data: List[int], n: int):
    line_colour = "#3572a5"
    plt.plot(list(range(len(data))), data, color=line_colour)
    plt.title(f"AoC 2020, day 15 part {n}")
    plt.xlabel("Iteration number")
    plt.ylabel("Value")


def visualise(instr: str):
    print("Running part one...")
    _, one = common.find_value_n(instr, 2020)
    print("Making graph")
    make_graph(one, 1)
    print("Saving")
    plt.savefig("0.png")
    plt.clf()
    print("Running part two...")
    _, two = common.find_value_n(instr, 30000000)
    print("Making graph")
    make_graph(two, 2)
    print("Saving low resolution")
    plt.savefig("1-lores.png")
    print("Saving high resolution")
    fig = plt.gcf()
    fig.set_size_inches(20.48, 10.8)
    fig.savefig("1-hires.png", dpi=100)
