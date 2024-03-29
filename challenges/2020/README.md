# Advent of Code 2020

Solutions to the [2020 Advent of Code](https://adventofcode.com/2020), in at least Python and Go. I make no claims that they're the best way to do things, but if they produce a result, I'm happy.

---

\* means that a given day has a visualisation

<!-- PARSE START -->

| Day                                |                    | Python                                   | Go                                   | Notes                |
| ---------------------------------- | ------------------ | ---------------------------------------- | ------------------------------------ | -------------------- |
| [1](01-reportRepair)               | Complete           | [Link](01-reportRepair/python)           | [Link](01-reportRepair/go)           |                      |
| [2](02-passwordPhilosophy)         | Complete           | [Link](02-passwordPhilosophy/python)     | [Link](02-passwordPhilosophy/go)     |                      |
| [3](03-tobogganTrajectory)         | Complete           | [Link](03-tobogganTrajectory/python)     | [Link](03-tobogganTrajectory/go)     |                      |
| [4](04-passportProcessing)         | Complete           | [Link](04-passportProcessing/python)     | [Link](04-passportProcessing/go)     |                      |
| [5](05-binaryBoarding)             | Complete           | [Link](05-binaryBoarding/python)         | [Link](05-binaryBoarding/go)         |                      |
| [6](06-customCustoms)              | Complete           | [Link](06-customCustoms/python)          | [Link](06-customCustoms/go)          |                      |
| [7](07-handyHaversacks)            | Complete           | [Link](07-handyHaversacks/python)        | [Link](07-handyHaversacks/go)        |                      |
| [8](08-handheldHalting)            | Complete           | [Link](08-handheldHalting/python)        | [Link](08-handheldHalting/go)        |                      |
| [9](09-encodingError)              | Complete           | [Link](09-encodingError/python)          | [Link](09-encodingError/go)          |                      |
| [10](10-adapterArray)              | Complete           | [Link](10-adapterArray/python)           | [Link](10-adapterArray/go)           |                      |
| [11](11-seatingSystem) \*          | Complete           | [Link](11-seatingSystem/python)          | [Link](11-seatingSystem/python)      |                      |
| [12](12-rainRisk) \*               | Complete           | [Link](12-rainRisk/python)               | [Link](12-rainRisk/go)               |                      |
| [13](13-shuttleSearch)             | Partially complete | [Link](13-shuttleSearch/python)          |                                      |                      |
| [14](14-dockingData)               | Complete           | [Link](14-dockingData/python)            | [Link](14-dockingData/go)            |                      |
| [15](15-rambunctiousRecitation) \* | Complete           | [Link](15-rambunctiousRecitation/python) | [Link](15-rambunctiousRecitation/go) |                      |
| [16](16-ticketTranslation)         | Complete           | [Link](16-ticketTranslation/python)      | [Link](16-ticketTranslation/go)      |                      |
| [17](17-conwayCubes)               | Partially complete | [Link](17-conwayCubes/python)            |                                      |                      |
| [18](18-operationOrder)            | Partially complete | [Link](18-operationOrder/python)         |                                      |                      |
| [19](19-monsterMessages)           | Complete           | [Link](19-monsterMessages/python)        | [Link](19-monsterMessages/go)        |                      |
| [20](20-jurassicJigsaw)            | Partially complete | [Link](20-jurassicJigsaw/python)         |                                      | Only part one solved |
| [21](21-allergenAmusement)         | Partially complete | [Link](21-allergenAmusement/python)      |                                      |                      |
| [22](22-crabCombat)                | Partially complete | [Link](22-crabCombat/python)             |                                      |                      |
| [23](23-crabCups)                  | Incomplete         |                                          |                                      |                      |
| [24](24-lobbyLayout)               | Partially complete | [Link](24-lobbyLayout/python)            |                                      |                      |
| [25](25-comboBreaker)              | Complete           | [Link](25-comboBreaker/python)           | [Link](25-comboBreaker/go)           |                      |

<!-- PARSE END -->

---

### Challenge summaries

**2020.01** - Find two/three numbers that sum to 2020

**2020.02** - Data validation

**2020.03** - Finding obstacles on a given path through a 2D array

**2020.04** - More data validation!

**2020.05** - Binary data/searching but also not

**2020.06** - Dealing with combinations of characters

**2020.07** - Dealing with large amounts of nested objects

**2020.08** - Write a simple interpreter with infinite loop detection, trial and error to find a value to modify

**2020.09** - Finding numbers that match different conditions within a sequence

**2020.10** - Finding permutations of a list that satisfy various constraints

**2020.11** - Build a custom cellular automata with weird neighborhoods

**2020.12** - Moving a virtual boat around a virtual sea with weird virtual instructions

**2020.13** - Chinese remainder theorem + buses = ???

**2020.14** - Funky bitmasks

**2020.15** - The Van Eck sequence

**2020.16** - Working out what values in a list means what by means of deduction and a set of rules

**2020.17** - ~~3D~~ **4**D cellular automata!

**2020.18** - Maths, but if BIDMAS didn't exist (the shunting yard algorithm)

**2020.19** - Generating regexes ~~as long as~~ longer than your arm and then making them recursive

**2020.20** - Solving a jigsaw programmatically and then looking for specific sequences of characters within the solved jigsaw

**2020.21** - Making deductions about values that are contained within multiple lists

**2020.22** - Simulating card games, and then making that card game recursive

**2020.23** - Crabs playing with cups

**2020.24** - Cellular automata, but this time with hexagons

**2020.25** - Reversing handshakes between a door and a RFID card (_"Unfortunately for the door, you know a thing or two about cryptographic handshakes"_)

---

![Lines of code per day](clocgraph.png)

_(Boilerplate code and code that generates visualisations is not included)_

---

<!-- RANK START -->

### Personal day-by-day stats

```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
 25   07:19:29   7966      0          -      -      -
 24   06:03:39   7277      0   06:50:17   6382      0
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