#!/usr/bin/env python3

import datetime
import requests
import json
import os
import sys
import argparse

script_dir = os.path.dirname(os.path.realpath(__file__))
default_config_file_name = os.path.join(script_dir, "input-loader.json")

today = datetime.date.today()

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "--config-file",
    dest="config_file",
    default=default_config_file_name,
    help="config file name",
)
parser.add_argument("--day", default=today.day, help="day to get input for")
parser.add_argument("--year", default=today.year, help="year to get input for")
parser.add_argument(
    "--stdout",
    default=False,
    action="store_true",
    help="send the input to stdout instead of a file",
)

args = parser.parse_args()

with open(args.config_file) as f:
    config_data = json.load(f)

r = requests.get(
    f"https://adventofcode.com/{args.year}/day/{args.day}/input",
    cookies={"session": config_data["session"]},
    headers={"User-Agent": config_data["userAgent"]},
)

if args.stdout:
    sys.stdout.write(r.text + "\n")
    sys.stderr.write("OK\n")
else:
    year_dir = os.path.join("challenges", str(args.year))
    directory_name = None
    for entry in os.listdir(year_dir):
        if entry.startswith(f"{args.day}-"):
            directory_name = entry
            break
    assert directory_name is not None, "challenge directory must already exist"
    path = os.path.join("challenges", str(args.year), directory_name, "input.txt")
    with open(path, "w") as f:
        f.write(r.text + "\n")

    sys.stderr.write(f"Written to {path}\n")
