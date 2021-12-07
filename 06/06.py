import numpy as np
from collections import defaultdict
from collections import Counter
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    int_list = list(map(int,input[0].split(",")))
    fish_age = 6
    for i in range(80):
        #print(int_list)
        new_int_list = []
        babies = []
        for index, _ in enumerate(int_list):
            cur_fish_age = int_list[index]
            cur_fish_age -= 1
            
            if cur_fish_age == -1:
                cur_fish_age = fish_age
                new_fish = fish_age+2
                babies.append(new_fish)
            new_int_list.append(cur_fish_age)
        new_int_list += babies
        int_list = new_int_list
    answer = len(int_list)
    return answer

def part2(input):
    int_list = list(map(int, input[0].split(",")))
    fish_age = 8
    bats_lijst = [int_list.count(i) for i in range(fish_age+1)]
    for i in range(256):
        nieuwe_bats_lijst = [0] * len(bats_lijst)
        for index, val in enumerate(bats_lijst):
            nieuwe_bats_lijst[index-1] = bats_lijst[index]
        nieuwe_bats_lijst[6] += bats_lijst[0]
        bats_lijst = nieuwe_bats_lijst

    answer = sum(bats_lijst)
    return answer

def part2_matrix(input):
    import io, numpy as np
    print('total after 256 day(s) is ' + str(np.sum(np.linalg.matrix_power(np.array(
        [[0, 1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.object),256).dot(np.array([[int(int(d)) for d in
                                                                                               io.open(
                                                                                                   "C:\\Users\\xxxx\\Advent of Code\\2021\\day 06 input.txt",
                                                                                                   "r",
                                                                                                   encoding="utf-8").readline().split(
                                                                                                   ',')].count(d) for d
                                                                                              in range(9)],
                                                                                             dtype=np.object)))))

run_program("test_input.txt")
run_program("input.txt")
