import json
import matplotlib.pyplot as plt
import os
import sys
import re

OUTPUT_FILE = sys.argv[1]
YEAR = sys.argv[2]

COLOURS = {
    "Golang": "#00ADD8",
    "Python": "#3572A5",
    "Nim": "#ffc200"
}

challenge_dir_regex = re.compile("""(?m)^(\d{2})-([a-zA-Z]+)$""")

directories = []
path = os.path.join("challenges", YEAR)
for filename in os.listdir(path):
    if os.path.isdir(os.path.join(path, filename)) and challenge_dir_regex.match(filename):
        directories.append(filename)

files = [os.path.join(x, "benchmark.json") for x in directories]

benchmark_data = {}

for filename in files:
    with open(os.path.join(path, filename)) as f:
        data = json.load(f)
    for language in data["implementations"]:
        x = benchmark_data.get(language, {})
        x[str(data["day"]) + ".1"] = data["implementations"][language]["part.1.avg"]
        x[str(data["day"]) + ".2"] = data["implementations"][language]["part.2.avg"]
        benchmark_data[language] = x

legends = []
all_days = set()

for language in benchmark_data:
    data = benchmark_data[language]
    part_one_times = []
    part_two_times = []
    days = []

    for key in data:
        
        day = int(key.split(".", 1)[0])
        if day not in days:
            days.append(day)
        all_days.add(day)

        if key.endswith(".1"):
            part_one_times.append(data[key])
        if key.endswith(".2"):
            part_two_times.append(data[key])
    
    line_colour = COLOURS.get(language)

    plt.plot(days, part_one_times, "o-", color=line_colour)
    plt.plot(days, part_two_times, "o--", color=line_colour)
    legends += [f"{language} part 1", f"{language} part 2"]

plt.title("Average challenge running time")

plt.xticks(list(all_days), [str(y) for y in all_days])
plt.ylabel("Running time (seconds)")
plt.xlabel("Day")

plt.legend(legends)

plt.savefig(OUTPUT_FILE)