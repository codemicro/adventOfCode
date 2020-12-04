import re

input_list = [x.replace("\n", " ") for x in open("input.txt").read().strip().split("\n\n")]

class Passport: 
    byr: str  # Birth year
    iyr: str  # Issue year
    eyr: str  # Expiration year
    hgt: str  # Height
    hcl: str  # Hair colour
    ecl: str  # Eye colour
    pid: str  # Passport ID
    cid: str  # Country ID

    def __init__(self, instr:str) -> None:
        self.byr = self._extract_field("byr", instr)
        self.iyr = self._extract_field("iyr", instr)
        self.eyr = self._extract_field("eyr", instr)
        self.hgt = self._extract_field("hgt", instr)
        self.hcl = self._extract_field("hcl", instr)
        self.ecl = self._extract_field("ecl", instr)
        self.pid = self._extract_field("pid", instr)
        self.cid = self._extract_field("cid", instr)

    def _extract_field(self, field:str, instr:str) -> str:
        matches = re.search(field + r":([^ ]+)", instr)
        if matches is None:
            return ""
        
        return matches.group(1)

    def validate(self) -> bool:
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if self.byr == "":
            return False
        if not (1920 <= int(self.byr) <= 2002):
            return False

        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if self.iyr == "":
            return False
        if not (2010 <= int(self.iyr) <= 2020):
            return False
        
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if self.eyr == "":
            return False
        if not (2020 <= int(self.eyr) <= 2030):
            return False

        # hgt (Height) - a number followed by either cm or in:
        #     If cm, the number must be at least 150 and at most 193.
        #     If in, the number must be at least 59 and at most 76.
        if self.hgt == "":
            return False
        if "cm" in self.hgt:
            if not (150 <= int(self.hgt.strip("cm")) <= 193):
                return False
        elif "in" in self.hgt:
            if not (59 <= int(self.hgt.strip("in")) <= 76):
                return False
        else:
            return False

        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if self.hcl == "":
            return False
        if self.hcl[0] == "#":
            if re.match(r"#[0-9a-f]{6}", self.hcl) is None:
                return False
        else:
            return False

        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        if self.ecl == "":
            return False
        if self.ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        if len(self.pid) == 9:
            try:
                int(self.pid)
            except ValueError:
                return False
        else:
            return False

        return True

passports = [Passport(x) for x in input_list]

valid_passports = 0
for passport in passports:
    if passport.validate():
        valid_passports += 1

print(f"There are {valid_passports} valid passports.")
