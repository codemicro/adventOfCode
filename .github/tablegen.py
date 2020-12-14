from datetime import datetime
import re
import sys
from bs4 import BeautifulSoup
import requests

today_day = datetime.now().day

readme_text = open(sys.argv[1]).read().strip().split("\n")

table_start_flag = "<!-- PARSE START -->"
table_end_flag = "<!-- PARSE END -->"

rank_start_flag = "<!-- RANK START -->"
rank_end_flag = "<!-- RANK END -->"

table_lines = []
in_table = False
for line in readme_text:
    line = line.strip()

    if line == table_end_flag:
        in_table = False
    if in_table:
        table_lines.append(line)
    elif line == table_start_flag:
        in_table = True

for i, l in enumerate(table_lines):
    rs = re.match(r"\|\s*(\d{1,})\s*\|\s*\|.+\|.+\|", l)
    if rs is not None and int(rs.group(1)) == today_day:

        table_lines[i] = f"| {today_day} | ![Not yet attempted][pending] | | |"

rank_lines = "### Personal day-by-day stats\n\n```".split("\n")
r = requests.get(
    "https://adventofcode.com/2020/leaderboard/self", cookies={"session": sys.argv[2]}
)
soup = BeautifulSoup(r.text, features="html.parser")
rank_lines += (
    soup.find("article")
    .get_text()
    .split("and 0 otherwise.")[-1]
    .strip("\n")
    .split("\n")
)
rank_lines += ["```"]

in_rank = False
table_appended = False
rank_appended = False
output = []
for i, line in enumerate(readme_text):
    line = line.strip()

    if line == table_start_flag:
        in_table = True
        output.append(table_start_flag)
        for ln in table_lines:
            output.append(ln)
    if line == table_end_flag:
        in_table = False

    if line == rank_start_flag:
        in_rank = True
        output.append(rank_start_flag)
        for ln in rank_lines:
            output.append(ln)
    if line == rank_end_flag:
        in_rank = False

    if in_rank or in_table:
        continue

    output.append(line)

open(sys.argv[1], "w").write("\n".join(output))
