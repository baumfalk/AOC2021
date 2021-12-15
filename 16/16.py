import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy

"0801"
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()
    
def neighbors_of_cell(pos, height, width, diagonal=False):
    y,x = pos
    # (dy == dx == 0) and (dy != 0 and dx != 0)
    def helper(x, dx, y, dy):
        if diagonal:
            horizontal_or_vertical = not (dy == 0 and dx == 0)
        else:
            horizontal_or_vertical = not (dy != 0 and dx != 0) and not (dy == 0 and dx==0)
        within_bounds = (0 <= y + dy < height) and (0 <= x + dx < width)
        return horizontal_or_vertical and within_bounds
    neighbors = {(y+dy,x+dx) for dy in [-1,0,1] for dx in [-1,0,1] if helper(x, dx, y, dy)}
    return neighbors

def part1(input):
    answer = None
    return answer


def part2(input):
    answer=None
    return answer


run_program("test_input.txt")
run_program("input.txt")
