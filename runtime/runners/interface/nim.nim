import std/strutils
import std/options
import std/json
import std/monotimes
import std/times

from nim/challenge as solutions import nil

proc sendResult(taskID: string, ok: bool, output: string, duration: float64) =
    let jobj = %* {
        "task_id": taskID,
        "ok": ok,
        "output": output,
        "duration": duration,
    }
    echo $jobj

type
    Task = ref object
        task_id: string
        part: int
        input: string
        output_dir: Option[string]

while true: 

    let
        taskString = readLine(stdin)
        task = to(parseJson(taskString), Task)    

    var runProc: proc(): string

    case task.part
    of 1:
        runProc = proc(): string = $(solutions.partOne(task.input))
    of 2:
        runProc = proc(): string = $(solutions.partTwo(task.input))
    else:
        sendResult(task.task_id, false, "unknown task part", 0.0)

    var
        result: string
        error: string

    let startTime = getMonoTime()
    try:
        result = runProc()
    except:
        error = getCurrentExceptionMsg()
    let endTime = getMonoTime()

    let runningTime = endTime - startTime
    let runningTimeSeconds = float(inNanoseconds(runningTime)) / float(1000000000)

    if error != "":
        sendResult(task.task_id, false, error, runningTimeSeconds)
    else:
        sendResult(task.task_id, true, result, runningTimeSeconds)