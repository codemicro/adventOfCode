from typing import *
from dataclasses import dataclass
from aocpy import BaseChallenge


class Path:
    parts: List[str]

    def __init__(self):
        self.parts = []

    def cd(self, arg: str):
        if arg == "..":
            _ = self.parts.pop()
        elif arg != ".":
            self.parts.append(arg)

    def cwd(self) -> str:
        x = "/".join(self.parts)
        return x if len(x) != 0 else "/"

    def abs_in_cwd(self, path: str) -> str:
        cwd = self.cwd()
        if cwd == "/":
            return "/" + path
        return cwd + "/" + path


@dataclass(init=False)
class Directories:
    directory_names: List[str]
    files: Dict[str, int]

    def __init__(self):
        self.directory_names = []
        self.files = {}

    def add_dir(self, path: str):
        if path not in self.directory_names:
            self.directory_names.append(path)

    def add_file(self, path: str, size: int):
        self.files[path] = size


def parse(instr: str) -> Directories:
    dirs = Directories()
    fp = Path()

    i = 0
    lines = instr.strip().splitlines()
    while i < len(lines):
        line = lines[i]

        if line.startswith("$ cd"):
            fp.cd(line.removeprefix("$ cd "))
            dirs.add_dir(fp.cwd())

        elif line.startswith("$ ls"):
            while i < len(lines) - 1 and not lines[i + 1].startswith("$"):
                i += 1
                line = lines[i]

                sp = line.split(" ")
                if sp[0] == "dir":
                    dirs.add_dir(fp.abs_in_cwd(sp[1]))
                else:
                    dirs.add_file(fp.abs_in_cwd(sp[1]), int(sp[0]))

        i += 1

    return dirs


def calculate_directory_size(dirs: Directories, target_dir_name: str) -> int:
    total = 0
    for fname in dirs.files:
        if fname.startswith(target_dir_name + "/"):
            total += dirs.files[fname]
    return total


class Challenge(BaseChallenge):
    @staticmethod
    def one(instr: str) -> int:
        dirs = parse(instr)

        total = 0

        for dir_name in dirs.directory_names:
            sz = calculate_directory_size(dirs, dir_name)
            if sz <= 100000:
                total += sz

        return total

    @staticmethod
    def two(instr: str) -> int:
        dirs = parse(instr)

        used = 70000000 - calculate_directory_size(dirs, "")
        amount_to_delete = 30000000 - used

        opts = []
        for dir_name in dirs.directory_names:
            sz = calculate_directory_size(dirs, dir_name)
            if sz >= amount_to_delete:
                opts.append(sz)

        return min(opts)
