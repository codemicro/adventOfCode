from datetime import datetime
import re
import sys

today_day = datetime.now().day

readme_text = open(sys.argv[1]).read().strip().split("\n")

start_flag = "<!-- PARSE START -->"
end_flag = "<!-- PARSE END -->"

table_lines = []
in_table = False
for line in readme_text:
    line = line.strip()

    if line == end_flag:
        in_table = False
    if in_table:
        table_lines.append(line)
    elif line == start_flag:
        in_table = True

for i, l in enumerate(table_lines):
    rs = re.match(r"\|\s*(\d{1,})\s*\|\s*\|.+\|.+\|", l)
    if rs is not None and int(rs.group(1)) == today_day:

        table_lines[i] = f"| {today_day} | ![Not yet attempted][pending] | | |"

counter = 0
for i, line in enumerate(readme_text):
    line = line.strip()

    if line == end_flag:
        in_table = False
    if in_table:
        readme_text[i] = table_lines[counter]
        counter += 1
    elif line == start_flag:
        in_table = True

open(sys.argv[1], "w").write("\n".join(readme_text))
