import sys
from collections import namedtuple
from enum import IntEnum


Module = namedtuple("Module", ["type", "name", "outputs"])
Pulse = namedtuple("Pulse", ["from", "to", "value"])


class PulseValue(IntEnum):
    LOW = 0
    HIGH = 1


def parse(instr: str) -> dict[str, Module]:
    x = {}

    for line in instr.splitlines():
        name, outputs = line.split(" -> ")
        module_type = None
        if not name[0].isalpha():
            module_type = name[0]
            name = name[1:]
        else:
            module_type = name
        
        x[name] = Module(module_type, name, outputs.split(", "))

    return x


def tick(modules: dict[str, Module], state: dict[str, any], pulses: list[Pulse]):
    next_pulses = []

    for pulse in pulses:
        dest_module = modules[pulse.to]
        
        match dest_module.type:
            case "broadcaster":
                for output in dest_module.outputs:
                    next_pulses.append(Pulse(dest_module.name, output, pulse.value))
            case "%":
                if pulse.value == PulseValue.LOW:
                    toggled = state.get(dest_module.name, False)
                    next_pulse_val = PulseValue.HIGH if toggled else PulseValue.LOW
                    for output in dest_module.outputs:
                        next_pulses.append(Pulse(dest_module.name, output, next_pulse_val))
                    state[dest_module.name] = not toggled
            case "&":
                state[dest_module.name] = state[dest_module.name] + [pulse]



def one(instr: str):
    modules = parse(instr)
    _debug(modules)
    return


def two(instr: str):
    return


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        sys.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))