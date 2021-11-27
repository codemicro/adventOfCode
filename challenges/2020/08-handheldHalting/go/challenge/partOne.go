package challenge

func PartOne(instr string) int {
	instructions := parse(instr)

	var (
		acc     int
		pc      int
		visited []int
	)

	for {
		{
			var found bool
			for _, v := range visited {
				if v == pc {
					found = true
					break
				}
			}
			if found {
				return acc
			} else {
				visited = append(visited, pc)
			}
		}

		cir := instructions[pc]

		if cir.Opcode == "jmp" {
			pc += cir.Operand
		} else {
			switch cir.Opcode {
			case "acc":
				acc += cir.Operand
			case "nop":
			}

			pc += 1

		}

	}
}
