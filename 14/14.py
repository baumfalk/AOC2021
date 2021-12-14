import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy

"0722"
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    cur_string = input[0]
    input = input[2:]
    rules = [line.split(" -> ") for line in input]
    rules_dict= {frm:to for frm,to in rules}
    for i in range(10):
        #print(cur_string)
        new_string = ""
        for index in range(len(cur_string)-1):
            pair = cur_string[index:index+2]
            if pair in rules_dict:
                char = rules_dict[pair]
                if index == 0:
                    new_string += pair[0] + char + pair[1]
                else:
                    new_string += char + pair[1]
            else:
                new_string += pair
                
        cur_string = new_string
        
    cntr = Counter(cur_string)
    
    answer=max(cntr.values()) - min(cntr.values())
    return answer

def part2(input):
    cur_string = input[0]
    input = input[2:]
    rules = [line.split(" -> ") for line in input]
    rules_dict = {frm: to for frm, to in rules}
    rules_dict2 = {frm: ((frm[0]+to),(to+frm[1])) for frm, to in rules}
    
    pair_counter = Counter()
    for index in range(len(cur_string)-1):
        pair_counter[cur_string[index:index+2]] +=1
    
    for i in range(40):
        #print(i, pair_counter)
        new_pair_counter = Counter()
        for pair in pair_counter:
            num_occurrences = pair_counter[pair]
            if num_occurrences == 0:continue

            #new_pair_counter[pair] = 0
            new_pairs = rules_dict2[pair]
            for new_pair in new_pairs:
                new_pair_counter[new_pair] += num_occurrences
        pair_counter = new_pair_counter
    
    letter_counter = Counter()
    for pair in pair_counter:
        num_occurrences = pair_counter[pair]
        first_letter,second_letter = list(pair)
        letter_counter[first_letter] += num_occurrences
        letter_counter[second_letter] += num_occurrences
    answer = (max(letter_counter.values())- min(letter_counter.values()))/2
    return np.ceil(answer), np.floor(answer)


run_program("test_input.txt")
run_program("input.txt")
