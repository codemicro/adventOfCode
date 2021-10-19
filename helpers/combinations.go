package helpers


// The following two functions were taken from https://stackoverflow.com/a/19249957

func GenerateCombinations(alphabet string, length int) <-chan string {
	c := make(chan string)
	go func(c chan string) {
		defer close(c)
		addLetter(c, "", alphabet, length)
	}(c)
	return c
}

func addLetter(c chan string, combo string, alphabet string, length int) {
	if length <= 0 {
		return
	}

	var newCombo string
	for _, ch := range alphabet {
		newCombo = combo + string(ch)
		c <- newCombo
		addLetter(c, newCombo, alphabet, length-1)
	}
}
