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
    from_to_lines = [line.split("-") for line in input]
    
    transitions = defaultdict(set)
    #G = nx.Graph()
    for frm, to in from_to_lines:
        transitions[frm].add(to)
        transitions[to].add(frm)
        #G.add_edge((frm, to))
    #nx.path
    
    paths = []
    last_num_paths = -1
    cur_node = "start"
    paths.append((["start"],set(["start"])))
    finished_paths = []
    visited_nodes = []
    while len(paths) > 0:
        last_num_paths = len(paths)
        cur_path,visited_smaller_nodes = paths[-1]
        paths = paths[:-1]
        cur_node = cur_path[-1]
        next_states = transitions[cur_node]
        new_paths = []
        for next_state in next_states:
            if (not next_state.islower()) or next_state not in visited_smaller_nodes:
                new_path = cur_path + [next_state]
                next_vis_smaller_nodes = copy.deepcopy(visited_smaller_nodes)
                if next_state.islower():
                    next_vis_smaller_nodes.add(next_state)
                if next_state == "end":
                    finished_paths.append((new_path, next_vis_smaller_nodes))
                else:
                    paths.append((new_path,next_vis_smaller_nodes))
                    
    #print(finished_paths)          
    #print(len(finished_paths))
   # state = np.array(list(map(lambda line: list(map(int, list(line))), input)))
   
    answer = len(finished_paths)
    return answer

def part2(input):
    from_to_lines = [line.split("-") for line in input]

    transitions = defaultdict(set)
    # G = nx.Graph()
    for frm, to in from_to_lines:
        transitions[frm].add(to)
        transitions[to].add(frm)
        # G.add_edge((frm, to))
    # nx.path

    paths = []
    last_num_paths = -1
    cur_node = "start"
    paths.append((["start"], Counter(["start"])))
    finished_paths = []
    visited_nodes = []
    while len(paths) > 0:
        last_num_paths = len(paths)
        cur_path, visited_smaller_nodes = paths[-1]
        paths = paths[:-1]
        cur_node = cur_path[-1]
        next_states = transitions[cur_node]
        new_paths = []
        for next_state in next_states:
            if next_state == "start":
                continue
            # not visited
            not_visited = next_state not in visited_smaller_nodes
            
            # or visited, and no other small caves are yet visited
            still_allowed = (sum(visited_smaller_nodes.values()) == len(visited_smaller_nodes.values()))
            visited_but_still_allowed = (next_state in visited_smaller_nodes) and still_allowed
            still_ok_to_visit = not_visited or visited_but_still_allowed
            #if next_state == "c":
            #    print(cur_path, visited_smaller_nodes, still_ok_to_visit)
            if (not next_state.islower()) or still_ok_to_visit:
                new_path = cur_path + [next_state]
                next_vis_smaller_nodes = copy.deepcopy(visited_smaller_nodes)
                if next_state.islower():
                    next_vis_smaller_nodes.update([next_state])
                if next_state == "end":
                    finished_paths.append((new_path, next_vis_smaller_nodes))
                else:
                    paths.append((new_path, next_vis_smaller_nodes))

    # print(finished_paths)          
    # print(len(finished_paths))
    # state = np.array(list(map(lambda line: list(map(int, list(line))), input)))

    answer = len(finished_paths)
    return answer


run_program("test_input.txt")
run_program("input.txt")
