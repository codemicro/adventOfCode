package challenge

import (
	"github.com/codemicro/adventOfCode/runtime/runners"
	"os"
	"strings"
)

func (c *Challenge) GetImplementations() ([]string, error) {
	dirEntries, err := os.ReadDir(c.Dir)
	if err != nil {
		return nil, err
	}

	var o []string
	for _, de := range dirEntries {
		if !de.IsDir() {
			continue
		}
		if _, ok := runners.Available[strings.ToLower(de.Name())]; ok {
			o = append(o, de.Name())
		}
	}

	return o, nil
}