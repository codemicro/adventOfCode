package challenge

import "errors"

func singleTransformation(v, subjectNumber int) int {
	return (v * subjectNumber) % 20201227
}

func transform(loopSize, subjectNumber int) int {
	v := 1
	for i := 0; i < loopSize; i += 1 {
		v = singleTransformation(v, subjectNumber)
	}
	return v
}

func findLoopSize(targetPubkey int) int {
	var c int
	v := 1
	for {
		c += 1
		v = singleTransformation(v, 7)
		if v == targetPubkey {
			return c
		}
	}
}

func PartOne(instr string) int {
	inputSlice := parse(instr)

	pubkeyOne := inputSlice[0]
	pubkeyTwo := inputSlice[1]

	loopSizeOne := findLoopSize(pubkeyOne)
	loopSizeTwo := findLoopSize(pubkeyTwo)

	encryptionKey := transform(loopSizeTwo, pubkeyOne)
	if encryptionKey != transform(loopSizeOne, pubkeyTwo) {
		panic(errors.New("encryption keys do not match"))
	}

	return encryptionKey
}
