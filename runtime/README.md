# AoC runtime

In brief: the runtime indexes available challenge implementations in the current working directory, loads inputs for a given challenge from disk and runs those inputs against a variety of available implementations for that challenge.

## Challenge discovery

The `./challenges` directory is indexed. Every subdirectory of `./challenges` is considered a "year". Every subdirectory within a given year that matches the regular expression `^(\d{2})-([a-zA-Z]+)$` (in practise, if it looks something like `05-somethingOrOther`) is considered a "challenge".

## Challenge data

Within every challenge, there should be a `info.json` file. This file should contain the filename of the main challenge input relative to the challenge directory and any test cases that can be run against a solution. An example is as follows:

```json
{
    "inputFile": "input.txt",
    "testCases": {
        "one": [
            {
                "input": "8A004A801A8002F478",
                "expected": "16"
            },
            {
                "input": "620080001611562C8802118E34",
                "expected": "12"
            }
        ],
        "two": [
            {
                "input": "C200B40A82",
                "expected": "3"
            },
            {
                "input": "04005AC33890",
                "expected": "54"
            },
            {
                "input": "880086C3E88112",
                "expected": "7"
            }
        ]
    }
}
```

## Challenge implementations

Any subdirectory in a challenge that has a name equal to one of the map keys defined in `Available` in [`./runners/runners.go`](./runners/runners.go) is considered a "challenge implementation".

## Running a challenge implementation

Once a challenge and implemetation has been selected, it is run by instantiating a runner inside the challenge directory. The type of runner is dependent on the challenge implementation selected.

Each runner will wrap the challenge code in some language specific wrapper code, then run that wrapper.

## Communicating with running challenges

Running challenge implemnentations recieve their inputs in JSON format, via `stdin`. A sample input might look like this:

```json
{"task_id": "test.1.0", "part": 1, "input": "8A004A801A8002F478"}
```

The running challenge implementation then processes the input, and returns a result via `stdout`, which might look soemthing like this:

```json
{"task_id": "test.1.0", "ok": true, "output": "16", "duration": 9.131431579589844e-05}
```

The format of both the input and output JSON is defined in [`./runners/comm.go`](./runners/comm.go) as the `Task` and `Result` structs.

The prefix of a task ID can be used within the wrapper to determine the type of task being run.

* A `test` prefix indicates a test is being run.
* A `main` prefix indicates that the main input is being used.
* A `vis` prefix indicates that a visualisation is being run.
* A `benchmark` prefix indicates that a given task is part of a benchmark.

**A running challenge implementation must return results in the same order they were returned in.**

## Debugging output

If anything is sent by a running challenge implementation via `stdout` that is not valid JSON, it will be passed through to the `stdout` of the runtime program.

## Stopping a running challenge implementation

There is no way for the runtime to communicate to a running implementation that it needs to shut down. Instead, the runtime forcibly kills the running implementation.