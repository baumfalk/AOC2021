from typing import List

import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy


def run_program(inp="input.txt"):
    # diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()


def neighbors_of_cell(pos, height=None, width=None, check_bounds=True, diagonal=False, include_self=False):
    y, x = pos

    # (dy == dx == 0) and (dy != 0 and dx != 0)
    def helper(x, dx, y, dy):
        if diagonal:
            horizontal_or_vertical = not (dy == 0 and dx == 0)
        else:
            horizontal_or_vertical = not (dy != 0 and dx != 0) and not (dy == 0 and dx == 0)
        
        within_bounds = (not check_bounds) or (0 <= y + dy < height) and (0 <= x + dx < width)
        return horizontal_or_vertical and within_bounds

    neighbors = [(y + dy, x + dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if helper(x, dx, y, dy)]
    if include_self: neighbors.append(pos)
    return sorted(neighbors)


def part1(input):
    algo = input[0]
    grid = input[2:]
    
    pixels = {}
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            pixels[(y,x)] = char
    old_pixels = copy.deepcopy(pixels)
    all_y, all_x = zip(*pixels.keys())
    min_y, max_y = min(all_y), max(all_y)
    min_x, max_x = min(all_x), max(all_x)
    # for y in range(min_y, max_y + 1):
    #     for x in range(min_x, max_x + 1):
    #         print(pixels[(y, x)], end="")
    #     print()
    # print()
    infinite_option = algo[0]
    all_option = algo[-1]
    for i in range(50):
        pixels = {}
        for pos in old_pixels:
            neighbors = neighbors_of_cell(pos,check_bounds=False,include_self=True,diagonal=True)
            lookup_binary_str = "".join([old_pixels.get(neighbor_pos,"." if i %2 == 0 or algo[0] == "." else "#")for neighbor_pos in neighbors])
            index = int(lookup_binary_str.replace("#","1").replace(".","0"),2)
            new_char = algo[index]
            pixels[pos] = new_char
            for neighbor in neighbors:
                if neighbor not in old_pixels:
                    neighbors_2 = neighbors_of_cell(neighbor, check_bounds=False, include_self=True, diagonal=True)
                    lookup_binary_str = "".join([old_pixels.get(neighbor_pos, "." if i %2 == 0 or algo[0] == "." else "#") for neighbor_pos in neighbors_2])
                    index = int(lookup_binary_str.replace("#", "1").replace(".", "0"), 2)
                    new_char = algo[index]
                    pixels[neighbor] = new_char
        old_pixels = copy.deepcopy(pixels)
        all_y, all_x = zip(*pixels.keys()) 
        min_y,max_y = min(all_y), max(all_y)
        min_x, max_x = min(all_x), max(all_x)
        # for y in range(min_y, max_y+1):
        #     for x in range(min_x, max_x + 1):
        #         print(pixels[(y,x)],end="")
        #     print()
        # print()
        
    answer = Counter(pixels.values())["#"]
    return answer


def part2(input):
    answer = None
    return answer


run_program("test_input.txt")
run_program("input.txt")
