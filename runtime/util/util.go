package util

import (
	"unicode"
)

func CamelToTitle(x string) string {
	var o string
	for i, char := range x {
		if i == 0 {
			o += string(unicode.ToUpper(char))
		} else if unicode.IsUpper(char) {
			o += " " + string(char)
		} else {
			o += string(char)
		}
	}
	return o
}