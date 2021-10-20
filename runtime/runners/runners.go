package runners

type Part uint8

const (
	PartOne Part = iota + 1
	PartTwo
	Visualise
)

type Runner interface {
	Queue(task *Task)
	Run() chan ResultOrError
}

type ResultOrError struct {
	Result *Result
	Error error
}

type RunnerCreator func(dir string) Runner

var Available = map[string]RunnerCreator{
	"py": newPythonRunner,
}

var RunnerNames = map[string]string{
	"py": "Python",
}