package challenge

import (
	"strconv"
	"strings"
)

type Instruction struct {
	Opcode  string
	Operand int
}

func NewInstruction(instr string) Instruction {
	icp := strings.Split(instr, " ")
	opc, err := strconv.Atoi(icp[1])
	if err != nil {
		panic(err)
	}
	return Instruction{
		Opcode:  icp[0],
		Operand: opc,
	}
}

func parse(instr string) (o []Instruction) {
	for _, v := range strings.Split(strings.TrimSpace(instr), "\n") {
		o = append(o, NewInstruction(v))
	}
	return
}
