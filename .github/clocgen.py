import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import json
import os
import sys


def best_fit(X, Y):

    xbar = sum(X) / len(X)
    ybar = sum(Y) / len(Y)
    n = len(X)  # or len(Y)

    numer = sum([xi * yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi ** 2 for xi in X]) - n * xbar ** 2

    b = numer / denum
    a = ybar - b * xbar

    return a, b


with open(sys.argv[1], errors="ignore") as f:
    cloc_results = json.loads(f.read())

python_by_day = {}
go_by_day = {}

for file in cloc_results["files"]:
    if file["language"].lower() == "python":
        target_dict = python_by_day
    elif file["language"].lower() == "go":
        target_dict = go_by_day
    else:
        continue

    split_name = file["name"].split(os.path.sep)
    if split_name[-1].lower() not in [
        "__main__.py",
        "main.go",
        "visualise.py",
        "visualise.go",
    ]:
        try:
            day_num = int(split_name[0].split("-")[0])
        except ValueError:
            continue

        if day_num not in target_dict:
            target_dict[day_num] = file["code"]
        else:
            target_dict[day_num] += file["code"]

print(python_by_day)
print(go_by_day)

days_array = [i + 1 for i in range(max(len(python_by_day), len(go_by_day)))]

# Add Python
python_colour = "#3572a5"

keys = list(sorted(python_by_day))
plt.plot(keys, [python_by_day[key] for key in keys], color=python_colour)
plt.scatter(keys, [python_by_day[key] for key in keys], color=python_colour, s=15)

a, b = best_fit(keys, [python_by_day[key] for key in keys])
yfit = [a + b * xi for xi in days_array]
plt.plot(days_array, yfit, color=python_colour, linestyle=":")

# Add Go
golang_colour = "#00add8"

keys = list(sorted(go_by_day))
plt.plot(keys, [go_by_day[key] for key in keys], color=golang_colour)
plt.scatter(keys, [go_by_day[key] for key in keys], color=golang_colour, s=15)

a, b = best_fit(keys, [go_by_day[key] for key in keys])
yfit = [a + b * xi for xi in days_array]
plt.plot(days_array, yfit, color=golang_colour, linestyle=":")

custom_lines = [
    Line2D([0], [0], color=python_colour, lw=2),
    Line2D([0], [0], color=golang_colour, lw=2),
]

plt.legend(custom_lines, ["Python", "Golang"])

plt.title("Lines of code by day")

plt.xticks(days_array)
plt.xlabel("Day")
plt.ylabel("Lines of code")

plt.savefig(sys.argv[2])
