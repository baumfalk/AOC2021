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


def insert_left(sommetje, number):
    # alleen getallen kunnen we toevoegen
    if number is None:
        return sommetje
    # print("il", sommetje, number)
    if type(sommetje) == int:
        return sommetje + number
    left_part, right_part = sommetje  # een sommetje heeft altijd een linkerdeel en een rechterdeel

    return [insert_left(left_part, number), right_part]


def insert_right(sommetje, number):
    # alleen getallen kunnen we toevoegen
    if number is None:
        return sommetje
    # print("ir", sommetje, number)
    if type(sommetje) == int:
        return sommetje + number
    left_part, right_part = sommetje  # een sommetje heeft altijd een linkerdeel en een rechterdeel

    return [left_part, insert_right(right_part, number)]


def explode(sommetje, depth=0):
    # print(sommetje)
    if type(sommetje) == int:
        return False, None, None, sommetje
    left_part, right_part = sommetje  # een sommetje heeft altijd een linkerdeel en een rechterdeel

    # To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.
    if depth == 4:
        return True, left_part, right_part, 0

    # we gaan van links naar rechts, dus eerst links proberen te exploden
    did_explode, to_inject_left, to_inject_right, left_part = explode(left_part, depth + 1)
    # als we links zijn geexplodeerd moeten we mogelijk nog wat rechts verwerken
    if did_explode:
        # print(f"left_exploded,depth: {depth},left_inject: {to_inject_left}, right_inject: {to_inject_right}, left_part:{left_part}, right_part:{right_part}, {sommetje}")
        # we moeten dit ding zo links mogelijk in het rechter sommetje proppen
        altered_right_part = insert_left(right_part, to_inject_right)
        nieuw_sommetje = [left_part, altered_right_part]
        to_inject_right = None
        return did_explode, to_inject_left, to_inject_right, nieuw_sommetje

    # anders zijn we links niet geexplode en gaan we kijken of we rechts kunnen exploderen
    did_explode, to_inject_left, to_inject_right, right_part = explode(right_part, depth + 1)

    # als we rechts zijn geexplodeerd moeten we mogelijk nog wat links verwerken
    if did_explode:
        # we moeten dit ding zo rechts mogelijk in het linker sommetje proppen
        altered_left_part = insert_right(left_part, to_inject_left)
        nieuw_sommetje = [altered_left_part, right_part]
        to_inject_left = None
        return did_explode, to_inject_left, to_inject_right, nieuw_sommetje

    # anders geven we gewoon onszelf terug
    return False, None, None, sommetje


def split(sommetje):
    import math
    # base case: we hebben 1 getal
    if type(sommetje) == int:
        if sommetje >= 10:
            return True, [math.floor(sommetje / 2), math.ceil(sommetje / 2)]
        else:
            return False, sommetje

    # we gaan van links naar rechts, dus eerst links proberen te splitsen
    left_part, right_part = sommetje
    did_split, left_part = split(left_part)
    if did_split:
        return did_split, [left_part, right_part]
    # als niet gesplit, dan rechts proberen
    did_split, right_part = split(right_part)
    # gesplit of niet, geeft terug wat we nu hebben
    return did_split, [left_part, right_part]


def reduce(sommetje):
    busy = True
    while busy:
        #print(sommetje)
        busy = False
        busy, _, _, sommetje = explode(sommetje)
        if not busy:
            busy, sommetje = split(sommetje)
    return sommetje

def add_fishes(fish_1, fish_2):
    return [fish_1, fish_2]

#sommetje = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
#print(reduce(sommetje))


def magnitude_fish(fish):
    left, right = fish
    num_left = left if type(left) == int else magnitude_fish(left)
    num_right = right if type(right) == int else magnitude_fish(right)
    return 3 * num_left + 2 * num_right


def part1(input):
    
    fishes = list(map(eval, input))
    
    cur_fish = add_fishes(fishes[0], fishes[1])
    cur_fish = reduce(cur_fish)
    for i in range(2,len(fishes)):
        cur_fish = add_fishes(cur_fish, fishes[i])
        cur_fish = reduce(cur_fish)
  
    #print(cur_fish)

    answer = magnitude_fish(cur_fish)
    return answer


def part2(input):
    answer = None
    fishes = list(map(eval, input))
    biggest_magnitude = 0
    for i in range(len(fishes)):
        for j in range(len(fishes)):
            if i ==j:continue
            cur_fish = add_fishes(fishes[i], fishes[j])
            cur_fish = reduce(cur_fish)
            biggest_magnitude = max(biggest_magnitude, magnitude_fish(cur_fish))
    answer = biggest_magnitude
    return answer


run_program("test_input.txt")
run_program("input.txt")
