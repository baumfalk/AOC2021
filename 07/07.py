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
    int_list = np.array(list(map(int,input[0].split(","))))
    return np.median(int_list)
    def cost_of_aligning(crabs, num):
        return np.sum(np.abs(crabs - num))
    cost = np.inf
    best_num = None
    
    for n in range(min(int_list), max(int_list)+1):
        new_cost = cost_of_aligning(int_list, n)
        if new_cost < cost:
            cost = new_cost
            best_num = n
    #print(cost_of_aligning(int_list, 2))
    return cost, best_num, np.median(int_list)
    #int_list = list(map(int, input)
    answer = None
    return answer

def part2(input):
    int_list = np.array(list(map(int, input[0].split(","))))
    mn = np.mean(int_list)
    mns = [np.floor(mn), np.ceil(mn)]
    def cost_of_aligning(crabs, num):
        num_steps_needed = np.abs(crabs - num)
        return np.sum(((num_steps_needed+1)*num_steps_needed)/2)
        #return np.sum(np.abs(crabs - num))
    return min(cost_of_aligning(int_list, mns[0]),cost_of_aligning(int_list, mns[1]))

    print(cost_of_aligning(int_list, 5))
    cost = np.inf
    best_num = None

    for n in range(min(int_list), max(int_list) + 1):
        new_cost = cost_of_aligning(int_list, n)
        if new_cost < cost:
            cost = new_cost
            best_num = n
    # print(cost_of_aligning(int_list, 2))
    return cost, best_num, np.mean(int_list)
    # int_list = list(map(int, input)
    answer = None
    return answer


run_program("test_input.txt")
run_program("input.txt")
