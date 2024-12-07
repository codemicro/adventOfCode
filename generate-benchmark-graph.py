#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys
from pathlib import Path

OUTPUT_FILE = sys.argv[1]
BENCHMARK_FILE = Path(sys.argv[2])

YEAR = BENCHMARK_FILE.parts[1]

COLOURS = {"Python": "#3572A5", "Go": "#00ADD8"}

MAX_Y_VALUE = 1

runner_translation = {
    "py": "Python",
    "go": "Go",
}

benchmark_data = {
    "Python": {},
    "Go": {},
}  # adding dicts here sets the order of points being plotted

with open(BENCHMARK_FILE) as f:
    for line in f.readlines():
        d = json.loads(line)
        rn = runner_translation[d["runner"]]
        benchmark_data[rn][f"{d['day']}.{d['part']}"] = d["avg"]

all_days = set()

for lang in benchmark_data:
    for key in benchmark_data[lang]:
        day = int(key.split(".", 1)[0])
        all_days.add(day)

figure = plt.figure(figsize=(25 / 2, 5))
axp1 = figure.add_subplot(1, 2, 1)
axp2 = figure.add_subplot(1, 2, 2, sharey=axp1)

axp1.axhline(y=15, color="#fc8080", linestyle="--")
axp2.axhline(y=15, color="#fc8080", linestyle="--")

for i, language in enumerate(benchmark_data):

    data = benchmark_data[language]
    
    part_one_times = []
    part_two_times = []

    p1days = []
    p2days = []

    for key in data:

        day = int(key.split(".", 1)[0])

        if key.endswith(".1"):
            if day not in p1days:
                p1days.append(day)
            part_one_times.append(data[key])
        if key.endswith(".2"):
            if day not in p2days:
                p2days.append(day)
            part_two_times.append(data[key])

    colour = COLOURS.get(language)

    p1 = axp1.scatter(p1days, part_one_times, color=colour)
    p2 = axp2.scatter(p2days, part_two_times, color=colour)

    for i, day in enumerate(p1days):
        if i + 1 >= len(p1days):
            continue
        if p1days[i + 1] == day + 1:
            axp1.plot(
                (day, p1days[i + 1]),
                (part_one_times[i], part_one_times[i + 1]),
                "-",
                color=colour,
            )
            
    for i, day in enumerate(p2days):
        if i + 1 >= len(p2days):
            continue
        if p2days[i + 1] == day + 1:
            axp2.plot(
                (day, p2days[i + 1]),
                (part_two_times[i], part_two_times[i + 1]),
                "-",
                color=colour,
            )

figure.suptitle(f"Average {YEAR} challenge running time")
axp1.set_title("Part one")
axp2.set_title("Part two")


def do_auxillary_parts(axis):
    plt.sca(axis)
    plt.xticks(list(all_days), [str(y) for y in all_days])
    plt.ylabel("Running time (log seconds)")
    plt.yscale("log")
    plt.xlabel("Day")
    plt.legend(
        handles=[patches.Patch(color=COLOURS[label], label=label) for label in COLOURS if len(benchmark_data[label]) > 0]
    )
    # plt.ylim([0, MAX_Y_VALUE])
    # plt.legend(legends)


do_auxillary_parts(axp1)
do_auxillary_parts(axp2)

plt.tight_layout()
plt.savefig(OUTPUT_FILE)
