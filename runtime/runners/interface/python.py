from py import Challenge

import time
import json

# TASKS_STR = input()
# TASKS = json.loads(TASKS_STR)


def send_result(task_id, ok, output, duration):
    print(
        json.dumps(
            {
                "task_id": task_id,
                "ok": ok,
                "output": str(output) if output is not None else "",
                "duration": float(duration),
            }
        ),
        flush=True,
    )


while True:
    task = json.loads(input())
    taskPart = task["part"]
    task_id = task["task_id"]

    run = None

    if taskPart == 1:
        run = lambda: Challenge.one(task["input"])
    elif taskPart == 2:
        run = lambda: Challenge.two(task["input"])
    elif taskPart == 3:
        run = lambda: Challenge.vis(task["input"], task["output_dir"])
    else:
        send_result(task_id, False, "unknown task part", 0)
        continue

    start_time = time.time()
    res = None
    err = None
    try:
        res = run()
    except Exception as e:
        err = f"{type(e)}: {e}"
        import traceback

        err = f"{type(e)}: {e}\n{''.join(traceback.format_tb(e.__traceback__))}"
    end_time = time.time()

    running_time = end_time - start_time

    if err is not None:
        send_result(task_id, False, err, running_time)
    else:
        send_result(task_id, True, res, running_time)
