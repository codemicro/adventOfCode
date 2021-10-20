package challenge

import (
	"encoding/json"
	"io/ioutil"
)

type Info struct {
	InputFile string `json:"inputFile"`
	TestCases struct {
		One []*TestCase `json:"one"`
		Two []*TestCase `json:"two"`
	} `json:"testCases"`
}

type TestCase struct {
	Input    string      `json:"input"`
	Expected interface{} `json:"expected"`
}

func LoadChallengeInfo(fname string) (*Info, error) {

	fcont, err := ioutil.ReadFile(fname)
	if err != nil {
		return nil, err
	}

	c := new(Info)
	err = json.Unmarshal(fcont, c)
	if err != nil {
		return nil, err
	}

	return c, nil
}
