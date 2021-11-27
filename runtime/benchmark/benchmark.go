package benchmark

import (
	"fmt"
	"github.com/codemicro/adventOfCode/runtime/challenge"
	"github.com/codemicro/adventOfCode/runtime/runners"
	"github.com/schollz/progressbar/v3"
	"io/ioutil"
	"path/filepath"
	"strings"
)

func makeBenchmarkID(part runners.Part, number int) string {
	if number == -1 {
		return fmt.Sprintf("benchmark.part.%d", part)
	}
	return fmt.Sprintf("benchmark.part.%d.%d", part, number)
}

func meanFloatSlice(arr []float64) float64 {
    var sum float64
    for _, v := range arr {
        sum += v
    }
    return sum / float64(len(arr))
}

func minFloatSlice(arr []float64) float64 {
    min := arr[0]
    for _, v := range arr {
        if v < min {
            min = v
        }
    }
    return min
}

func maxFloatSlice(arr []float64) float64 {
    max := arr[0]
    for _, v := range arr {
        if v > max {
            max = v
        }
    }
    return max
}

func Run(selectedChallenge *challenge.Challenge, input string, numberRuns int) error {

	implementations, err := selectedChallenge.GetImplementations()
	if err != nil {
		return err
	}

	var valueSets []*values

	for _, implementation := range implementations {
		v, err := benchmarkImplementation(implementation, selectedChallenge.Dir, input, numberRuns)
		if err != nil {
			return err
		}
		valueSets = append(valueSets, v)
	}

	// make file
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("Day %d (%s) benchmark\n\n", selectedChallenge.Number, selectedChallenge.Name))
	sb.WriteString(fmt.Sprintf("Dir: %s\n", selectedChallenge.Dir))
	sb.WriteString(fmt.Sprintf("Runs per part: %d\n", numberRuns))

	for _, vs := range valueSets {
		sb.WriteString("--------------------------------------------------------------------------------\n")
		sb.WriteString(vs.implementation)
		sb.WriteString("\n\n")
		for _, v := range vs.values {
			sb.WriteString(fmt.Sprintf("%s: %f seconds\n", v.key, v.value))
		}
	}
	sb.WriteString("--------------------------------------------------------------------------------\n")

	fpath := filepath.Join(selectedChallenge.Dir, "benchmark.txt")

	fmt.Println("Writing results to", fpath)

	return ioutil.WriteFile(
		fpath,
		[]byte(sb.String()),
		0644,
	)
}

type values struct {
	implementation string
	values []kv
}

type kv struct {
    key string
    value float64
}

func benchmarkImplementation(implementation string, dir string, inputString string, numberRuns int) (*values, error) {

	var results []*runners.Result

	runner := runners.Available[implementation](dir)
	for i := 0; i < numberRuns; i++ {

		runner.Queue(&runners.Task{
			TaskID: makeBenchmarkID(runners.PartOne, i),
			Part:   runners.PartOne,
			Input:  inputString,
		})

		runner.Queue(&runners.Task{
			TaskID: makeBenchmarkID(runners.PartTwo, i),
			Part:   runners.PartTwo,
			Input:  inputString,
		})

	}

	pb := progressbar.NewOptions(
		numberRuns * 2, // two parts means 2x the number of runs
		progressbar.OptionSetDescription(
			fmt.Sprintf("Running %s benchmarks", runners.RunnerNames[implementation]),
		),
	)

	res, cleanup := runner.Run()

	for roe := range res {
		if roe.Error != nil {
			_ = pb.Close()
			return nil, roe.Error
		}
		results = append(results, roe.Result)
		_ = pb.Add(1)
	}

	fmt.Println()
	pb = progressbar.NewOptions(
		len(results) + 1, // two parts means 2x the number of runs
		progressbar.OptionSetDescription(
			fmt.Sprintf("Processing %s results", runners.RunnerNames[implementation]),
		),
	)

	var (
		p1, p2 []float64
		p1id = makeBenchmarkID(runners.PartOne, -1)
		p2id = makeBenchmarkID(runners.PartTwo, -1)
	)

	for _, result := range results {
		if strings.HasPrefix(result.TaskID, p1id) {
			p1 = append(p1, result.Duration)
		} else if strings.HasPrefix(result.TaskID, p2id) {
			p2 = append(p2, result.Duration)
		}
		_ = pb.Add(1)
	}

	_ = pb.Finish()
	fmt.Println()

	if cleanup != nil {
		cleanup()
	}

	return &values{
		implementation: runners.RunnerNames[implementation],
		values: []kv{
			{"benchmark.part.1.avg", meanFloatSlice(p1)},
			{"benchmark.part.1.min", minFloatSlice(p1)},
			{"benchmark.part.1.max", maxFloatSlice(p1)},
			{"benchmark.part.2.avg", meanFloatSlice(p2)},
			{"benchmark.part.2.min", minFloatSlice(p2)},
			{"benchmark.part.2.max", maxFloatSlice(p2)},
		},
	}, nil
}