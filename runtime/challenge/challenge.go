package challenge

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/codemicro/adventOfCode/runtime/util"
)

type Challenge struct {
	Number int
	Name   string
	Dir string
}

func (c *Challenge) String() string {
	return fmt.Sprintf("%d - %s", c.Number, c.Name)
}

var challengeDirRegexp = regexp.MustCompile(`(?m)^(\d{2})-([a-zA-Z]+)$`)

func ListingFromDir(sourceDir string) ([]*Challenge, error) {

	dirEntries, err := os.ReadDir(sourceDir)
	if err != nil {
		return nil, err
	}

	var o []*Challenge
	for _, entry := range dirEntries {

		if entry.IsDir() && challengeDirRegexp.MatchString(entry.Name()) {
			dir := entry.Name()

			x := strings.Split(dir, "-")
			dayInt, _ := strconv.Atoi(x[0]) // error ignored because regex should have ensured this is ok
			dayTitle := util.CamelToTitle(x[1])
			o = append(o, &Challenge{
				Number: dayInt,
				Name:   dayTitle,
				Dir:    filepath.Join(sourceDir, dir),
			})

		}

	}

	return o, nil
}
