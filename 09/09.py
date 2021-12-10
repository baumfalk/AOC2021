import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re

def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    int_list = np.array(list(map(lambda line: list(map(int,list(line))),input)))
    #int_list = np.genfromtxt(input, delimiter=1).astype(int)
    #input_proc = list(map(lambda s: s.split(" | "), input))
   
    counter = 0
    risk_points = 0
    for y in range(int_list.shape[0]):
        for x in range(int_list.shape[1]):
            val = int_list[y][x]
            still_possible = True
            for dy in [-1,0,1]:
                new_y = y + dy

                if new_y < 0 or new_y >= int_list.shape[0]:
                    continue
                for dx in [-1,0,1]:
                    new_x = x+dx
                    
                    if new_x < 0 or new_x >= int_list.shape[1]:
                        continue
                    
                    new_val = int_list[new_y][new_x]
                    if new_val < val:
                        still_possible = False
                        break
            if still_possible:
                counter+=1
                risk_points += 1 + int_list[y][x]

    answer = risk_points
    return answer

def part2(input):
    int_list = np.array(list(map(lambda line: list(map(int, list(line))), input)))
    # int_list = np.genfromtxt(input, delimiter=1).astype(int)
    # input_proc = list(map(lambda s: s.split(" | "), input))

    counter = 0
    risk_points = 0
    risk_locs = []
    #vind minima
    for y in range(int_list.shape[0]):
        for x in range(int_list.shape[1]):
            val = int_list[y][x]
            still_possible = True
            for dy in [-1, 0, 1]:
                new_y = y + dy

                if new_y < 0 or new_y >= int_list.shape[0]:
                    continue
                for dx in [-1, 0, 1]:
                    new_x = x + dx

                    if new_x < 0 or new_x >= int_list.shape[1]:
                        continue

                    new_val = int_list[new_y][new_x]
                    if new_val < val:
                        still_possible = False
                        break
            if still_possible:
                counter += 1
                risk_points += 1 + int_list[y][x]
                risk_locs.append((y,x))
    basins = {}           
    for risk_loc in risk_locs:
        basin = set()
        basin.add(risk_loc)
        locs_to_check = [risk_loc]
        locs_to_check_set = set([risk_loc])
        #bfs
        while len(locs_to_check_set):
            y,x = locs_to_check[0]
            locs_to_check = locs_to_check[1:]
            locs_to_check_set.remove((y,x))
            for dy in [-1, 0, 1]:
                new_y = y + dy
                if new_y < 0 or new_y >= int_list.shape[0]:
                    continue       
                for dx in [-1, 0, 1]:
                    new_x = x + dx
                    if new_x < 0 or new_x >= int_list.shape[1] or (dx != 0 and dy != 0):
                        continue
                    value = int_list[new_y][new_x]
                    # 9 is muur
                    if value != 9 and (new_y, new_x) not in basin and (new_y, new_x) not in locs_to_check_set:
                        locs_to_check.append((new_y, new_x))
                        locs_to_check_set.add((new_y, new_x))
                        basin.add((new_y, new_x))
        basins[risk_loc] = len(basin)
    
    total = 1
    # alleen de top 3 pakken, niet alles :clown:
    for basin_size in sorted(list(basins.values()),reverse=True)[:3]:
        total *= basin_size
        
    answer = total
    return answer

def part2_onepass(input):
    int_list = np.array(list(map(lambda line: list(map(int, list(line))), input)))
    
    basins = {}
    loc_to_basin = {}
    
    
    for y in range(int_list.shape[0]):
        for x in range(int_list.shape[0]):
            value = int_list[y,x]

run_program("test_input.txt")
run_program("input.txt")
