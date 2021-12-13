import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    
    dict_coords = set()
    
    def fold(coords, dimension, n):
        
        """
        
        fold along y, 7
        0,14 -> 0,0
        0,13 -> 0,1
        0,12 -> 0,2
        """
        new_coords = set()

        for y,x in coords:
            if dimension == "y":
                new_x = x
                if y >= n:
                    new_y = n - (y - n)
                else:
                    new_y = y
                new_coords.add((new_y, new_x))
            else:
                if x >= n:
                    new_x = n - (x - n)
                else:
                    new_x = x
                new_y = y
                new_coords.add((new_y, new_x))
        return new_coords
    
    for line in input:
        if line.startswith("fold"):
            l,r = line.split("=")
            dimension = l[-1]
            coord = int(r)
            dict_coords = fold(dict_coords,dimension, coord)
            #print(len(dict_coords))
            pass
        elif line == "":
            pass
        else:
            x,y = line.split(",")
            x = int(x)
            y = int(y)
            dict_coords.add((y,x))
        
    
    #lines = [line.split("-") for line in input]
    
    answer = len(dict_coords)
    array = np.zeros((100,100))
    
    for y,x in dict_coords:
        array[y,x]=1
        
    print(array)
    return answer

def part2(input):
    #from_to_lines = [line.split("-") for line in input]

    answer = None
    return answer


run_program("test_input.txt")
run_program("input.txt")
