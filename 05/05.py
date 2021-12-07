import numpy as np
from collections import defaultdict
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    
    cell_counter = defaultdict(int)
    for line in input:
        left, right = line.split(" -> ")
        from_x, from_y = list(map(int,left.split(",")))
        to_x, to_y = list(map(int,right.split(",")))
        
        
        #horizontal/vertical
        if not (from_x == to_x or from_y == to_y):
            continue
        
        from_x, to_x = min(from_x, to_x), max(from_x, to_x)
        from_y, to_y = min(from_y, to_y), max(from_y, to_y)
        
        for cur_x in range(from_x, to_x+1):
            for cur_y in range(from_y, to_y + 1):
                cell_counter[(cur_y,cur_x)] += 1
                
    total = 0
    for pair in cell_counter:
        if cell_counter[pair] > 1:
            total+=1
    answer = total
    return answer

def part2(input):
    cell_counter = defaultdict(int)
    for line in input:
        left, right = line.split(" -> ")
        from_x, from_y = list(map(int, left.split(",")))
        to_x, to_y = list(map(int, right.split(",")))
        
        if not (from_x == to_x or from_y == to_y):
            # diagonal
            modifier_x = 1 if from_x <= to_x else -1
            modifier_y = 1 if from_y <= to_y else -1
            from_real_x, to_real_x = min(from_x, to_x), max(from_x, to_x)
            nums = [(from_x + i*modifier_x,from_y+i*modifier_y) for i,_ in enumerate(range(from_real_x, to_real_x + 1))]
            for cur_x,cur_y in nums:
                cell_counter[(cur_y, cur_x)] += 1
        else:
            from_x, to_x = min(from_x, to_x), max(from_x, to_x)
            from_y, to_y = min(from_y, to_y), max(from_y, to_y)
        
            for cur_x in range(from_x, to_x + 1 if from_x <= to_x else -1, 1 if from_x <= to_x else -1):
                for cur_y in range(from_y, to_y + 1 if from_y <= to_y else -1, 1 if from_y <= to_y else -1):
                    cell_counter[(cur_y, cur_x)] += 1

    total = 0
    
    for pair in cell_counter:
        if cell_counter[pair] > 1:
            total += 1
    answer = total
    return answer

run_program("test_input.txt")
run_program("input.txt")
