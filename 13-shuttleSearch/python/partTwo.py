def partTwo(instr: str) -> int:
    # This is the parsing section
    service_list = instr.strip().split("\n")[-1].split(",")

    eqns = []
    for i, svc in enumerate(service_list):
        if svc == "x":
            continue
        svc = int(svc)

        v = 0
        if i != 0:
            v = svc - i  # This is the only maths stuff in the parsing

        eqns.append((v, svc))

    # This is the maths section

    n = 1
    for (_, v) in eqns:
        n *= v

    sigma_x = 0
    for (bi, ni) in eqns:
        # this type cast could potentially cause a problem.
        # int required for pow function and the division *should* produce a whole number anyway
        Ni = int(n / ni)
        yi = pow(Ni, -1, ni)  # https://stackoverflow.com/a/9758173
        sigma_x += bi * Ni * yi

    return sigma_x % n
