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
    #lines = [line.split("-") for line in input]
   
    answer = None
    return answer

def part2(input):
    #from_to_lines = [line.split("-") for line in input]

    answer = None
    return answer


run_program("test_input.txt")
run_program("input.txt")
