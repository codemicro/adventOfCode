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

func IntPermutations(arr []int) [][]int {
	var helper func([]int, int)
	res := [][]int{}

	helper = func(arr []int, n int) {
		if n == 1 {
			tmp := make([]int, len(arr))
			copy(tmp, arr)
			res = append(res, tmp)
		} else {
			for i := 0; i < n; i++ {
				helper(arr, n-1)
				if n%2 == 1 {
					tmp := arr[i]
					arr[i] = arr[n-1]
					arr[n-1] = tmp
				} else {
					tmp := arr[0]
					arr[0] = arr[n-1]
					arr[n-1] = tmp
				}
			}
		}
	}
	helper(arr, len(arr))
	return res
}

func StringPermutations(x string) []string {
	var asInts []int
	for _, char := range x {
		asInts = append(asInts, int(char))
	}
	ip := IntPermutations(asInts)
	var o []string
	for _, x := range ip {
		var b string
		for _, y := range x {
			b += string(rune(y))
		}
		o = append(o, b)
	}
	return o
}