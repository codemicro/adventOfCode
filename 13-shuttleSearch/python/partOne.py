from typing import List


class Timetable:
    earliest_departure: int
    services: List[int]

    def __init__(self, earliest_departure: int, services: str):
        self.earliest_departure = earliest_departure
        self.services = [int(s) for s in services.split(",") if s != "x"]


def parse(instr: str) -> Timetable:
    instr = instr.strip().split("\n")
    return Timetable(int(instr[0]), instr[1])


def partOne(instr: str) -> int:
    timetable = parse(instr)

    earliest_times = []
    for service in timetable.services:
        earliest_times.append(
            (service, (int(timetable.earliest_departure / service) + 1) * service)
        )

    route, earliest_departure = min(earliest_times, key=lambda x: x[1])

    return route * (earliest_departure - timetable.earliest_departure)
