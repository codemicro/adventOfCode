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

BAR_WIDTH = 0.45
datasets = []

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
                p1days.append(day - (BAR_WIDTH / 2))
            part_one_times.append(data[key])
        if key.endswith(".2"):
            if day not in p2days:
                p2days.append(day + (BAR_WIDTH / 2))
            part_two_times.append(data[key])

    if len(part_one_times) == 0 and len(part_two_times) == 0:
        break

    datasets.append(((p1days, part_one_times), (p2days, part_two_times), language))

figure = plt.figure(figsize=(6 * len(datasets), 5))

fst = None
for i, (partone, parttwo, label) in enumerate(datasets):
    axp = figure.add_subplot(1, len(datasets), i + 1, sharey=fst)
    if fst is None:
        fst = axp

    axp.bar(*partone, color="#fb4934", width=BAR_WIDTH)
    axp.bar(*parttwo, color="#fabd2f", width=BAR_WIDTH)

    axp.axhline(y=15, color="#fc8080", linestyle="--")
    axp.set_title(label)

    plt.sca(axp)
    plt.xticks(list(all_days), [str(y) for y in all_days])
    plt.ylabel("Running time (log seconds)")
    plt.yscale("log")
    plt.xlabel("Day")
    plt.legend(
        handles=[
            patches.Patch(color="#fb4934", label="Part one"),
            patches.Patch(color="#fabd2f", label="Part two"),
        ]
    )


figure.suptitle(f"{YEAR} challenge running time")

plt.tight_layout()
plt.savefig(OUTPUT_FILE)
