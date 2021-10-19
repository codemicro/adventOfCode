package helpers

// The following two functions were taken and/or modified from https://stackoverflow.com/a/29023392

func CartesianProduct(a []int, k int) <-chan []int {
	c := make(chan []int)	
	lens := len(a)
	r := make([]int, k)
	
	go func(c chan []int) {
		defer close(c)
		for ix := make([]int, k); ix[0] < lens; nextIndex(ix, lens) {
			for i, j := range ix {
				r[i] = a[j]
			}
			c <- r
		}
	}(c)

	return c
}

// nextIndex sets ix to the lexicographically next value,
// such that for each i>0, 0 <= ix[i] < lens.
func nextIndex(ix []int, lens int) {
	// https://stackoverflow.com/a/29023392
	for j := len(ix) - 1; j >= 0; j-- {
		ix[j]++
		if j == 0 || ix[j] < lens {
			return
		}
		ix[j] = 0
	}
}
