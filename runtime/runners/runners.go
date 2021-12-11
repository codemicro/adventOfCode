package runners

type Part uint8

const (
	PartOne Part = iota + 1
	PartTwo
	Visualise
)

type Runner interface {
	Start() error
	Stop() error
	Cleanup() error
	Run(task *Task) (*Result, error)
}

type ResultOrError struct {
	Result *Result
	Error error
}

type RunnerCreator func(dir string) Runner

var Available = map[string]RunnerCreator{
	"py": newPythonRunner,
	"go": newGolangRunner,
	//"nim": newNimRunner,
}

var RunnerNames = map[string]string{
	"py": "Python",
	"go": "Golang",
	//"nim": "Nim",
}