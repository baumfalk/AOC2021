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
    print(part2_clean(content))
    print()
    
def part1(input):
    #int_list = np.array(list(map(int,input[0].split(","))))
    input_proc = list(map(lambda s: s.split(" | "), input))
    input_proc2 = list(map(lambda s: s[1].split(" "), input_proc))
    
    lookup = {1:2, 4:4, 7:3, 8: 7}
    lookup_rev = {2:1, 4:4, 3:7, 7:8}
    total = 0
    for line in input_proc2:
        for elem in line:
            if len(elem) in lookup_rev:
                total += 1#lookup_rev[len(elem)]
    answer = total
    return answer

def part2(inp):
    #int_list = np.array(list(map(int, input[0].split(","))))
    input_proc = list(map(lambda s: s.split(" | "), inp))
    input_proc_left = list(map(lambda s: s[0].split(" "), input_proc))
    input_proc_left = list(map(lambda line: list(map(lambda wires: frozenset(wires),line)), input_proc_left))
    
    input_proc_right = list(map(lambda s: s[1].split(" "), input_proc))
    input_proc_right = list(map(lambda l: list(map(frozenset,l)), input_proc_right))

    lookup = {1: 2, 4: 4, 7: 3, 8: 7}
    lookup_rev = {2: 1, 4: 4, 3: 7, 7: 8}
     
    final_wire_lookup = {}
    final_num_lookup = {frozenset("abcefg"):0, frozenset("cf"): 1,frozenset("acdef"):2,
                       frozenset("acdfg"):3, frozenset("bcdf"):4, frozenset("abdfg"):5,
                        frozenset("abdefg"):6, frozenset("acf"):7, frozenset("abcdefg"):8,
                        frozenset("abcdfg"):9}
    total = 0
    for index in range(len(inp)):
        left = input_proc_left[index]
        right = input_proc_right[index]
        
        lookup_local = {lookup_rev.get(len(wires)):wires for wires in left if lookup_rev.get(len(wires))}
        extract_a = lookup_local[7] - lookup_local[1]
        extract_bd = lookup_local[4] - lookup_local[1]
        final_wire_lookup["a"]=list(extract_a)[0]
        extract_9 = [wires for wires in left if len(wires) == 6 and wires.intersection(lookup_local[7]) == lookup_local[7] and wires.issuperset(extract_bd)]
        lookup_local[9] = extract_9[0]
        extract_e = lookup_local[8] - lookup_local[9]
        final_wire_lookup["e"] = list(extract_e)[0]
        extract_3 = [wires for wires in left if len(wires) == 5 and final_wire_lookup["e"] not in wires and wires.issuperset(lookup_local[7])]
        lookup_local[3] = extract_3[0]
        extract_2 = [wires for wires in left if
                     len(wires) == 5 and final_wire_lookup["e"] in wires]
        lookup_local[2] = extract_2[0]
        
        extract_6 = [wires for wires in left if wires not in lookup_local.values() and len(wires) == 6 and
                     len(wires.intersection(lookup_local[4])) == 3 and len(wires.intersection(lookup_local[7])) == 2]
        lookup_local[6] = extract_6[0]

        extract_5 = [wires for wires in left if wires not in lookup_local.values() and len(wires) == 5]
        lookup_local[5] = extract_5[0]
        extract_0 = [wires for wires in left if wires not in lookup_local.values() ]
        lookup_local[0] = extract_0[0]

        lookup_local_reverse = {item:key for key,item in lookup_local.items()}
        # extract_f = lookup_local[3] - lookup_local[2]
        # final_wire_lookup["f"] = list(extract_f)[0]
        # extract_b = lookup_local[4] - lookup_local[3]
        # final_wire_lookup["b"] = list(extract_b)[0]
        # extract_d = extract_bd - extract_b
        # final_wire_lookup["d"] = list(extract_d)[0]
        # extract_c = lookup_local[7] - extract_a - extract_f
        # final_wire_lookup["c"] = list(extract_c)[0]
        # extract_g = lookup_local[8] - extract_a - extract_b - extract_c - extract_d - extract_e - extract_f
        # final_wire_lookup["g"] = list(extract_g)[0]
        
        num = ""
        for number_wired in right:
            num += str(lookup_local_reverse[number_wired])
            #print(lookup_local_reverse[number_wired],end="")
        #print()
        num = int(num)
        total += num
        # 7 is acf
        
    answer = total
    return answer

def part2_clean(input):
    data = list(map(lambda s: list(zip(map(lambda y: y.split(" "),s.split(" | ")))), input))
    res = 0
    for a, b in data:
        a = a[0]
        b = b[0]
        d = dict()
        for word in sorted(a, key=len):
            word = set(word)
            l = len(word)
            if   l == 2: d[1] = word
            elif l == 3: d[7] = word
            elif l == 4: d[4] = word
            elif l == 7: d[8] = word
            elif l == 5:
                if   len(word & d[7]) == 3: d[3] = word
                elif len(word & d[4]) == 3: d[5] = word
                else:                       d[2] = word
            elif l == 6:
                if len(word & d[5]) == 5:
                    if len(word & d[7]) == 2: d[6] = word
                    else:                     d[9] = word
                else:                         d[0] = word
        digits = (str(k) for digit in b
                         for k, v in d.items()
                         if set(digit) == v)
        res += int("".join(digits))
    return res

run_program("test_input.txt")
run_program("input.txt")
