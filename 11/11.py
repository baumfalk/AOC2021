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
    state = np.array(list(map(lambda line: list(map(int, list(line))), input)))
    def neighbor(y,x, dims):
        neighbors = []
        for dy in [-1,0,1]:
            next_y = y + dy
            if next_y < 0 or next_y >= dims[0]:
                continue
            for dx in [-1,0,1]:
                next_x = x + dx
                if next_x < 0 or next_x >= dims[1]:
                    continue
                if dx == 0 == dy:
                    continue
                neighbors.append((next_y, next_x))
        return neighbors
    n_steps = 100
    
    def next_state(state):
        new_state = copy.deepcopy(state)
        new_state = new_state + 1
        new_state_2 = copy.deepcopy(state)
        exploded_already = set()
        prev_len_exploded = -1
        flashes = 0
        while len(exploded_already) != prev_len_exploded:
            prev_len_exploded = len(exploded_already)
            for y in range(new_state.shape[0]):
                for x in range(new_state.shape[1]):
                    if new_state[y,x] > 9:
                        flashes += 1
                        exploded_already.add((y,x))
                        new_state[y,x] = 0
                        neigbors = neighbor(y,x,state.shape)
                        for y_n, x_n in neigbors:
                            if (y_n, x_n) not in exploded_already:
                                new_state[y_n, x_n] += 1
        return new_state, flashes
    n_flashes = 0
    for i in range(n_steps):
        #print(i)
        #print(state)
        #print()
        state, flashes = next_state(state)
        
        n_flashes += flashes
    answer = n_flashes
    return answer

def part2(input):
    state = np.array(list(map(lambda line: list(map(int, list(line))), input)))

    def neighbor(y, x, dims):
        neighbors = []
        for dy in [-1, 0, 1]:
            next_y = y + dy
            if next_y < 0 or next_y >= dims[0]:
                continue
            for dx in [-1, 0, 1]:
                next_x = x + dx
                if next_x < 0 or next_x >= dims[1]:
                    continue
                if dx == 0 == dy:
                    continue
                neighbors.append((next_y, next_x))
        return neighbors

    n_steps = 1000

    def next_state(state):
        new_state = copy.deepcopy(state)
        new_state = new_state + 1
        new_state_2 = copy.deepcopy(state)
        exploded_already = set()
        prev_len_exploded = -1
        flashes = 0
        while len(exploded_already) != prev_len_exploded:
            prev_len_exploded = len(exploded_already)
            for y in range(new_state.shape[0]):
                for x in range(new_state.shape[1]):
                    if new_state[y, x] > 9:
                        flashes += 1
                        exploded_already.add((y, x))
                        new_state[y, x] = 0
                        neigbors = neighbor(y, x, state.shape)
                        for y_n, x_n in neigbors:
                            if (y_n, x_n) not in exploded_already:
                                new_state[y_n, x_n] += 1
        return new_state, flashes

    n_flashes = 0
    for i in range(n_steps):
        state, flashes = next_state(state)

        n_flashes += flashes

        if np.sum(state) == 0:
            answer = i + 1
            break
    return answer


run_program("test_input.txt")
run_program("input.txt")
