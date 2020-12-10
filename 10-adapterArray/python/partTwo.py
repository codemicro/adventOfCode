def partTwo(instr: str) -> int:
    joltages = sorted([int(x) for x in instr.strip().split("\n")])

    route_lengths = {0: 1}
    for joltage in joltages:
        total_routes = 0
        # Get the route lengths for the three previous joltages
        for n in [1, 2, 3]:
            total_routes += route_lengths.get(joltage - n, 0) 
        print(joltage, total_routes)
        route_lengths[joltage] = total_routes

    return route_lengths[max(joltages)]
