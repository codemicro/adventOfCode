package challenge

func execute(instructions []Instruction) (cleanExit bool, acc int) {
	var (
		pc      int
		visited []int
	)

	for {
		if pc >= len(instructions) {
			// Clean exit
			return true, acc
		}

		{
			var found bool
			for _, v := range visited {
				if v == pc {
					found = true
					break
				}
			}
			if found {
				return false, acc
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

func PartTwo(instr string) int {
	masterInstructions := parse(instr)

	var switchSetLocations []int
	for idx, instruction := range masterInstructions {
		if instruction.Opcode == "jmp" || instruction.Opcode == "nop" {
			switchSetLocations = append(switchSetLocations, idx)
		}
	}

	for _, slc := range switchSetLocations {
		// Copy instruction set
		instructions := make([]Instruction, len(masterInstructions))
		copy(instructions, masterInstructions)

		// Swap instruction
		oldval := instructions[slc].Opcode
		var newval string
		if oldval == "jmp" {
			newval = "nop"
		} else if oldval == "nop" {
			newval = "jmp"
		}
		instructions[slc].Opcode = newval

		// Execute
		cleanExit, acc := execute(instructions)
		if cleanExit {
			return acc
		}
	}

	return 0
}
