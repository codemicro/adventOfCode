package aocgo

import "errors"

type BaseChallenge struct{}

func (b BaseChallenge) One(instr string) (interface{}, error) {
	return nil, errors.New("not implemented")
}

func (b BaseChallenge) Two(instr string) (interface{}, error) {
	return nil, errors.New("not implemented")
}

func (b BaseChallenge) Vis(instr string, outdir string) error {
	return errors.New("not implemented")
}
