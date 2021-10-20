package challenge

import (
	"encoding/json"
	"io/ioutil"
)

type ChallengeInfo struct {
	InputFile string `json:"inputFile"`
	TestCases struct {
		One []struct {
			Input    string `json:"input"`
			Expected int64  `json:"expected"`
		} `json:"one"`
		Two []struct {
			Input    string `json:"input"`
			Expected int    `json:"expected"`
		} `json:"two"`
	} `json:"testCases"`
}

func LoadChallengeInfo(fname string) (*ChallengeInfo, error) {

	fcont, err := ioutil.ReadFile(fname)
	if err != nil {
		return nil, err
	}

	c := new(ChallengeInfo)
	err = json.Unmarshal(fcont, c)
	if err != nil {
		return nil, err
	}

	return c, nil
}