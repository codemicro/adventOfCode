from typing import List, Set    
import re


class Tile:
    components: List[List[str]]
    edges: Set[str]
    number: int

    def __init__(self, instr:str) -> None:
        split_input = instr.strip().split("\n")
        self.number = int(re.search(r"Tile (\d+)", split_input[0]).group(1))
        self.components = [list(x) for x in split_input[1:]]
        
        self.edges = []
        self.edges.append(split_input[1])
        self.edges.append(split_input[-1])
        self.edges.append("".join([self.components[x][0] for x in range(len(self.components))]))
        self.edges.append("".join([self.components[x][-1] for x in range(len(self.components))]))


def parse(instr: str) -> List[Tile]:
    return [Tile(x) for x in instr.strip().split("\n\n")]
