# Advent of Code 🎄

Jump to: [2020](challenges/2020) - [2021](challenges/2021) - [2022](challenges/2022) - [2023](challenges/2023) - [2024](challenges/2024)

Solutions to [Advent of Code](https://adventofcode.com) challenges.

Puzzle inputs and descriptions are not included in this repository. You'll have to get these yourself from the AoC website. [Here's why](https://www.reddit.com/r/adventofcode/comments/k99rod/sharing_input_data_were_we_requested_not_to/gf2ukkf/?context=3).

[AoC website](https://adventofcode.com) - [AoC subreddit](https://www.reddit.com/r/adventofcode) - [AoC awesome list](https://github.com/Bogdanp/awesome-advent-of-code)

## Running solutions

The method of running solutions varies by year.

<details><summary><b>From 2023 onwards</b></summary>

Use the `./aoc` script and provide it with the filename of the file you would like to run. For example, `./aoc run challenges/01-trebuchet/main.py`.

Alternatively, run the code directly. Provide it with an input via stdin and set the first command line argument to be either `1` or `2` to run either part 1 or 2 respectively. This should go for all languages.

</details>

<details><summary><b>2021 and 2022</b></summary>

In order to run solutions from 2021 and 2022, you should switch to the `2022` branch first.

Solutions to 2021's and 2022's solutions are run via the runner program contained in [`./runtime`](./runtime).

To run a solution, run `go run github.com/codemicro/adventOfCode/runtime` and follow the on-screen prompts. Configurisation options can be seen by running with the `--help` flag.

A benchmark graph can be generated using [`generate-benchmark-graph.py`](./generate-benchmark-graph.py) as follows: `python3 generate-benchmark-graph.py <output file> <year>`.

For example, to generate a graph for the 2021 benchmarks and save it to `challenges/2021/running-times.png`, you can run `python3 generate-benchmark-graph.py challenges/2021/running-times.png 2021`.
</details>

<details><summary><b>2020</b></summary>

In 2020, all solutions are in Python and/or Go.

1. `cd` to the challenge directory
   eg: `cd challenges/2020/05-binaryBoarding`
2. Run the desired implementation
   * For Python, run `python3 ./py`
   * For Go, run `go run ./go`

Dependencies for 2020 challenges are not neatly defined anywhere, so determing and installing the correct ones is an exercise for the reader.

</details>
