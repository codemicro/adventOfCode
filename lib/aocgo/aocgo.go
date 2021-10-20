package aocgo

import "errors"

type BaseChallenge struct{}

func (b *BaseChallenge) one(instr string) (interface{}, error) {
	return nil, errors.New("not implemented")
}

func (b *BaseChallenge) two(instr string) (interface{}, error) {
	return nil, errors.New("not implemented")
}

func (b *BaseChallenge) vis(instr string, outdir string) error {
	return errors.New("not implemented")
}
