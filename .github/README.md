# Advent of Code 2020

Solutions to the [2020 Advent of Code](https://adventofcode.com/2020), in at least Python and Go. I make no claims that they're the best way to do things, but if they produce a result within 15 seconds, I'm happy.

Go solutions are near direct copies of the Python solutions and may be added a few days afterwards.

Puzzle inputs and descriptions are not included in this repository. You'll have to get these yourself from the AoC website. [Here's why](https://www.reddit.com/r/adventofcode/comments/k99rod/sharing_input_data_were_we_requested_not_to/gf2ukkf/?context=3).

[AoC website](https://adventofcode.com) - [AoC subreddit](https://www.reddit.com/r/adventofcode) - [AoC awesome list](https://github.com/Bogdanp/awesome-advent-of-code)

---

**Key:** ![Completed][check] is completed, ![Incomplete][cross] is incomplete, ![Partially complete][partial] is partially complete (does not have both languages or does not have solutions to both parts) and ![Not yet attempted][pending] is released but not yet attempted. \* means that this day has a visualisation

<!-- PARSE START -->

| Day                                 |                                | Python                                    | Go                                    | Notes                |
| ----------------------------------- | ------------------------------ | ----------------------------------------- | ------------------------------------- | -------------------- |
| [1](/01-reportRepair)               | ![Completed][check]            | [Link](/01-reportRepair/python)           | [Link](/01-reportRepair/go)           |                      |
| [2](/02-passwordPhilosophy)         | ![Completed][check]            | [Link](/02-passwordPhilosophy/python)     | [Link](/02-passwordPhilosophy/go)     |                      |
| [3](/03-tobogganTrajectory)         | ![Completed][check]            | [Link](/03-tobogganTrajectory/python)     | [Link](/03-tobogganTrajectory/go)     |                      |
| [4](/04-passportProcessing)         | ![Completed][check]            | [Link](/04-passportProcessing/python)     | [Link](/04-passportProcessing/go)     |                      |
| [5](/05-binaryBoarding)             | ![Completed][check]            | [Link](/05-binaryBoarding/python)         | [Link](/05-binaryBoarding/go)         |                      |
| [6](/06-customCustoms)              | ![Completed][check]            | [Link](/06-customCustoms/python)          | [Link](/06-customCustoms/go)          |                      |
| [7](/07-handyHaversacks)            | ![Completed][check]            | [Link](/07-handyHaversacks/python)        | [Link](/07-handyHaversacks/go)        |                      |
| [8](/08-handheldHalting)            | ![Completed][check]            | [Link](/08-handheldHalting/python)        | [Link](/08-handheldHalting/go)        |                      |
| [9](/09-encodingError)              | ![Completed][check]            | [Link](/09-encodingError/python)          | [Link](/09-encodingError/go)          |                      |
| [10](/10-adapterArray)              | ![Completed][check]            | [Link](/10-adapterArray/python)           | [Link](/10-adapterArray/go)           |                      |
| [11](/11-seatingSystem) \*          | ![Completed][check]            | [Link](/11-seatingSystem/python)          | [Link](/11-seatingSystem/python)      |                      |
| [12](/12-rainRisk) \*               | ![Completed][check]            | [Link](/12-rainRisk/python)               | [Link](/12-rainRisk/go)               |                      |
| [13](/13-shuttleSearch)             | ![Partially complete][partial] | [Link](/13-shuttleSearch/python)          |                                       |                      |
| [14](/14-dockingData)               | ![Completed][check]            | [Link](/14-dockingData/python)            | [Link](/14-dockingData/go)            |                      |
| [15](/15-rambunctiousRecitation) \* | ![Completed][check]            | [Link](/15-rambunctiousRecitation/python) | [Link](/15-rambunctiousRecitation/go) |                      |
| [16](/16-ticketTranslation)         | ![Partially complete][partial] | [Link](/16-ticketTranslation/python)      |                                       |                      |
| [17](/17-conwayCubes)               | ![Partially complete][partial] | [Link](/17-conwayCubes/python)            |                                       |                      |
| [18](/18-operationOrder)            | ![Partially complete][partial] | [Link](/18-operationOrder/python)         |                                       |                      |
| [19](/19-monsterMessages)           | ![Completed][check]            | [Link](/19-monsterMessages/python)        | [Link](/19-monsterMessages/go)        |                      |
| [20](/20-jurassicJigsaw)            | ![Partially complete][partial] | [Link](/20-jurassicJigsaw/python)         |                                       | Only part one solved |
| [21](/21-allergenAmusement)         | ![Partially complete][partial] | [Link](/21-allergenAmusement/python)      |                                       |                      |
| [22](/22-crabCombat)                | ![Partially complete][partial] | [Link](/22-crabCombat/python)             |                                       |                      |
| 23                                  | ![Not yet attempted][pending]  |                                           |                                       |                      |
| 24                                  |                                |                                           |                                       |                      |
| 25                                  |                                |                                           |                                       |                      |

<!-- PARSE END -->

---

![Lines of code per day](https://github.com/codemicro/adventOfCode/blob/master/.github/clocgraph.png?raw=true)

_(Boilerplate code and code that generates visualisations is not included)_

---

<!-- RANK START -->

### Personal day-by-day stats

```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
 22   06:37:56   9949      0   07:46:00   7333      0
 21   07:07:02   7031      0   07:34:43   6897      0
 20   12:40:05   9000      0          -      -      -
 19   07:14:52   7163      0   10:08:56   6083      0
 18   13:02:40  15057      0   17:01:47  15031      0
 17   19:16:58  17492      0   19:48:07  16771      0
 16   08:37:03  16270      0   11:24:49  13401      0
 15   11:38:11  20197      0   11:50:13  18272      0
 14   13:01:47  20661      0   14:41:22  17482      0
 13   05:43:41  16692      0   07:55:25   9661      0
 12   07:49:19  18545      0   09:08:54  16885      0
 11   12:07:36  24295      0   12:38:25  19932      0
 10   13:38:25  35155      0   15:10:40  24968      0
  9   12:26:06  34364      0   12:55:00  32791      0
  8   06:56:11  26688      0   07:13:46  22653      0
  7   12:03:04  29181      0   13:02:47  25777      0
  6   05:03:12  23094      0   05:22:54  21650      0
  5   06:42:59  25458      0   07:27:47  25658      0
  4   04:59:28  26236      0   11:53:07  34630      0
  3   07:18:34  33113      0   13:03:50  45815      0
  2   11:33:00  47471      0   11:38:14  44961      0
  1   18:09:35  65566      0   18:12:26  60825      0
```

<!-- RANK END -->

[check]: https://github.com/codemicro/adventOfCode/blob/master/.github/check.png?raw=true
[cross]: https://github.com/codemicro/adventOfCode/blob/master/.github/cross.png?raw=true
[partial]: https://github.com/codemicro/adventOfCode/blob/master/.github/partial.png?raw=true
[pending]: https://github.com/codemicro/adventOfCode/blob/master/.github/asterisk.png?raw=true
