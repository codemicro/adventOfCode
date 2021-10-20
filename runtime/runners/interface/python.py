from py import Challenge

import time
import json

TASKS_STR = """{{ .TasksJSON }}"""
TASKS = json.loads(TASKS_STR)

def send_result(task_number, ok, output, duration):
    print(json.dumps({
        "task_n": task_number,
        "ok": ok,
        "output": str(output) if output is not None else "",
        "duration": float(duration),
    }), flush=True)

for task_number, task in enumerate(TASKS):
    taskPart = task["part"]

    run = None

    if taskPart == 1:
        run = lambda: Challenge().one(task["input"])
    elif taskPart == 2:
        run = lambda: Challenge().two(task["input"])
    elif taskPart == 3:
        run = lambda: Challenge().vis(task["input"], task["output_dir"])
    else:
        send_result(task_number, False, "unknown task part", 0)
        continue

    start_time = time.time()
    res = None
    err = None
    try:
        res = run()
    except Exception as e:
        err = f"{type(e)}: {e}"
    end_time = time.time()

    running_time = end_time-start_time

    if err is not None:
        send_result(task_number, False, err, running_time)
    else:
        send_result(task_number, True, res, running_time)
