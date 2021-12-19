from typing import List

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
    
def neighbors_of_cell(pos, height, width, diagonal=False):
    y,x = pos
    # (dy == dx == 0) and (dy != 0 and dx != 0)
    def helper(x, dx, y, dy):
        if diagonal:
            horizontal_or_vertical = not (dy == 0 and dx == 0)
        else:
            horizontal_or_vertical = not (dy != 0 and dx != 0) and not (dy == 0 and dx==0)
        within_bounds = (0 <= y + dy < height) and (0 <= x + dx < width)
        return horizontal_or_vertical and within_bounds
    neighbors = {(y+dy,x+dx) for dy in [-1,0,1] for dx in [-1,0,1] if helper(x, dx, y, dy)}
    return neighbors

class Pair:
    def __init__(self, left, right, path, depth):
        self.left = left
        self.right = right
        self.path = path
        self.depth = depth
    
    def is_single_val(self):
        return self.left is None or self.right is None
    
    def get_single_val(self):
        if not self.is_single_val():
            raise Exception()
        if self.left is not None:
            return self.left
        return self.right

    def add_to_single_val(self, val):
        if not self.is_single_val():
            raise Exception()
        if self.left is not None:
            self.left += val
        else:
            self.right += val
            
    def set_other_val(self, val):
        if not self.is_single_val():
            raise Exception()
        if self.left is not None:
            self.right = val
        else:
            self.left = val
    
    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.path == other.path and self.depth == other.depth
    
    def __repr__(self):
        return f"{self.left, self.right, self.path, self.depth}"

def list_to_tuple(lst):
    left, right = lst
    left = left if type(left) == int else list_to_tuple(left)
    right = right if type(right) == int else list_to_tuple(right)
    return (left, right)

def flatten_list(lst, path= "",depth=0):
    left, right = lst
    if type(left) == int:
        if type(right) == int:
            return [Pair(left, right, path, depth)]
        else:
            left_part = [Pair(left, None, path,depth)]
            right_part = flatten_list(right, path+"1", depth + 1)
    else:
        left_part = flatten_list(left, path+"0", depth + 1)
        if type(right) == int:
            right_part = [Pair(None, right, path, depth)]
        else:
            right_part = flatten_list(right, path+"1",depth + 1)
    return left_part + right_part

def reduce(fish):
    done = False
    while not done:
        print(fish)
        done = True
        old_fish = copy.deepcopy(fish)
        fish = explode_fish(fish)
        if old_fish != fish:
            done = False
        if done:  # exploding failed, time to split
            fish = split(fish)
            if old_fish != fish:
                done = False
    return fish

def split(fish: List[Pair]):
    new_fish = []
    already_splitted = False
    for i, cur_pair in enumerate(fish):
        if already_splitted:
            new_fish.append(cur_pair)
        else:
            if cur_pair.is_single_val():
                if cur_pair.get_single_val() >= 10:
                    already_splitted = True
                    val = cur_pair.get_single_val()
                    val_left, val_right = val // 2, np.ceil(val / 2).astype(int)
                    cur_pair.left = val_left
                    cur_pair.right = val_right
                    new_fish.append(cur_pair)
                else:
                    new_fish.append(cur_pair)
            elif cur_pair.left >= 10:
                already_splitted = True
                new_pair_left = Pair(cur_pair.left // 2, np.ceil(cur_pair.left / 2).astype(int), cur_pair.path+"0", cur_pair.depth + 1)
    
                new_fish.append(new_pair_left)
                if cur_pair.right is not None:
                    new_pair_right = Pair(None, cur_pair.right, cur_pair.path,cur_pair.depth)
                    new_fish.append(new_pair_right)
            elif cur_pair.right >= 10:
                already_splitted = True
                new_pair_right = Pair(cur_pair.right // 2, np.ceil(cur_pair.right / 2).astype(int), cur_pair.path+"1",cur_pair.depth + 1)
                if cur_pair.left is not None:
                    new_pair_left = Pair(cur_pair.left, None, cur_pair.path,cur_pair.depth)
                    new_fish.append(new_pair_left)
                new_fish.append(new_pair_right)
            else:
                new_fish.append(cur_pair)

    return new_fish

def explode_fish(fish: List[Pair]):
    new_fish = []
    already_exploded = False
    for i, cur_pair in enumerate(fish):
        if cur_pair.depth == 4 and not already_exploded:
            already_exploded = True
            # if both sides
            if i > 0 and i < len(fish) -1:
                prev_pair = fish[i - 1]
                next_pair = fish[i + 1]
                if prev_pair.is_single_val() and next_pair.is_single_val():
                    prev_pair.add_to_single_val(cur_pair.left)
                    next_pair.add_to_single_val(cur_pair.right)
                    #prev_pair.left += cur_pair.left
                    #next_pair.right += cur_pair.right
                    
                    # de nul voegen we toe waar we de grootste overlap hebben
                    overlap_prev = len([1 for index,bit in enumerate(prev_pair.path) if index < len(cur_pair.path) and bit == cur_pair.path[index]])
                    overlap_next = len([1 for index, bit in enumerate(next_pair.path) if
                                       index < len(cur_pair.path) and bit == cur_pair.path[index]])
                    if overlap_next > overlap_prev:
                        next_pair.set_other_val(0)
                    else:
                        prev_pair.set_other_val(0)
                elif prev_pair.is_single_val():
                    prev_pair.left += cur_pair.left
                    next_pair.left += cur_pair.right

                    prev_pair.right = 0
                elif next_pair.is_single_val():
                    next_pair.right += cur_pair.right
                    prev_pair.right += cur_pair.left
                    next_pair.left = 0
                else:
                    overlap_prev = len([1 for index, bit in enumerate(prev_pair.path) if
                                        index < len(cur_pair.path) and bit == cur_pair.path[index]])
                    overlap_next = len([1 for index, bit in enumerate(next_pair.path) if
                                        index < len(cur_pair.path) and bit == cur_pair.path[index]])
                    # if overlap_next > overlap_prev:
                    #     next_pair.set_other_val(0)
                    prev_pair.right += cur_pair.left
                    next_pair.left += cur_pair.right
                    if overlap_next > overlap_prev:
                        cur_pair.left = 0
                        cur_pair.right = None
                    else:
                        cur_pair.left = None
                        cur_pair.right = 0
                    cur_pair.path = cur_pair.path[:-1]
                    cur_pair.depth -=1
                    new_fish.append(cur_pair)
                    #print("paniekk2")
            elif i > 0:
                prev_pair = fish[i - 1]
                if prev_pair.right is not None:
                    new_pair = Pair(None, 0, cur_pair.path[:-1], cur_pair.depth - 1)
                    new_fish.append(new_pair)
                    prev_pair.right += cur_pair.left
                    # if prev_pair.depth == cur_pair.depth - 1:
                    #     prev_pair.right = 0
                else:
                    prev_pair.left += cur_pair.left
                    if prev_pair.depth == cur_pair.depth - 1:
                        prev_pair.right = 0
            elif i < len(fish) - 1:
                next_pair = fish[i + 1]
                if next_pair.left is not None:
                    new_pair = Pair(0,None, cur_pair.path[:-1],cur_pair.depth-1)
                    new_fish.append(new_pair)
                    next_pair.left += cur_pair.right
                else:
                    next_pair.right += cur_pair.right
                    if next_pair.depth == cur_pair.depth - 1:
                        next_pair.left = 0
        else:
            new_fish.append(cur_pair)
    return new_fish

def add_fishes(fish_1, fish_2):
    for f in fish_1:
        f.depth+=1
        f.path = "1"+f.path
    for f in fish_2:
        f.depth+=1
        f.path = "0"+f.path

    return fish_1 + fish_2

def part1(input):
    
    fishes = list(map(lambda x: flatten_list(eval(x)), input))
    
    cur_fish = add_fishes(fishes[0], fishes[1])
    cur_fish = reduce(cur_fish)
    for i in range(2,len(fishes)):
        cur_fish = add_fishes(cur_fish, fishes[i])
        cur_fish = reduce(cur_fish)
    print(cur_fish)
    
    
    def magnitude_fish(fish):
        left, right = fish
        num_left = left if type(left) == int else magnitude_fish(left)
        num_right = right if type(right) == int else magnitude_fish(right)
        return 3* num_left + 2*num_right
    
    
    answer = None
    return answer


def part2(input):
    answer = None
    return answer


run_program("test_input.txt")
#run_program("input.txt")
