import sys


def parse(f):
    yield [char == "#" for char in f.readline().rstrip()]
    f.readline()
    yield {
        (x, y) for y, line in enumerate(f) for x, char in enumerate(line) if char == "#"
    }


def index(x, y, is_light):
    i = 0
    for ny in range(y - 1, y + 2):
        for nx in range(x - 1, x + 2):
            i = i << 1 | is_light(nx, ny)
    return i


def enhance(light, algo, step):
    xmin = min(x for x, y in light)
    xmax = max(x for x, y in light)
    ymin = min(y for x, y in light)
    ymax = max(y for x, y in light)

    def is_light(x, y):
        if algo[0] and not (xmin <= x <= xmax and ymin <= y <= ymax):
            return step % 2
        return (x, y) in light

    return {
        (x, y)
        for y in range(ymin - 1, ymax + 2)
        for x in range(xmin - 1, xmax + 2)
        if algo[index(x, y, is_light)]
    }


def enhance_times(light, algo, times):
    for step in range(times):
        light = enhance(light, algo, step)
    return light


with open("input.txt") as f:
    algo, light = parse(f)
print(len(enhance_times(light, algo, 2)))
print(len(enhance_times(light, algo, 50)))
