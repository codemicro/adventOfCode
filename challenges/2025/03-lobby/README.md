# [Day 3: Lobby](https://adventofcode.com/2025/day/3)

The key insight:

 * When you are selecting `n` batteries from a bank, you must select one such that there are `n-1` batteries in the bank after it
 * As overall joltages are concatenated, the first battery you select from the bank will be the most significant (ie. if you are selecting 3, the first battery you select will represent hundreds). Therefore, to get the largest possible overall joltage, you want to select the highest number from the set of numbers that you have to choose from
 * Then, you repeat for `n-1` batteries, but only using numbers that are after the number you just chose