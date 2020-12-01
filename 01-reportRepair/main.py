input_string = open("input.txt").read().strip().split("\n")

values = [int(x) for x in inputString]

for i in values:
    for v in values:
        if v + i == 2020:
            print("Part one answer is:", v * i)

print()

for i in values:
    for v in values:
        for x in values:
            if v + i + x == 2020:
                print("Part two answer is:", v * i * x)
