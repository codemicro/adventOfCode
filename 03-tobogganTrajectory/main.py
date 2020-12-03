input_list = open("input.txt").read().strip().split("\n")

forest = [[char for char in line] for line in input_list]

tree_char = "#"

def find_collisions(forest:list, x_offset:int, y_offset:int) -> int:
    encountered_trees = 0
    x_pointer = 0

    for row in forest[::y_offset]:
        target_index = x_pointer % len(row)
        if row[target_index] == tree_char:
            encountered_trees += 1
        x_pointer += x_offset

    return encountered_trees

offset_pairs = [
    (3, 1),
    (1, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

tree_product = 1

for i, pair in enumerate(offset_pairs):
    encountered_trees = find_collisions(forest, *pair)
    tree_product *= encountered_trees
    print(f"Pair {pair}: {encountered_trees} trees", ("(part one solution)" if i == 0 else ""))

print(f"Product of all: {tree_product} (part two solution)")