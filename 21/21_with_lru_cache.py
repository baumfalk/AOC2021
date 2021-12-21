from typing import List

import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy
import itertools
from functools import lru_cache

"0725"
def run_program(inp="input.txt"):
    # diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()


def neighbors_of_cell(pos, height=None, width=None, check_bounds=True, diagonal=False, include_self=False):
    y, x = pos

    # (dy == dx == 0) and (dy != 0 and dx != 0)
    def helper(x, dx, y, dy):
        if diagonal:
            horizontal_or_vertical = not (dy == 0 and dx == 0)
        else:
            horizontal_or_vertical = not (dy != 0 and dx != 0) and not (dy == 0 and dx == 0)

        within_bounds = (not check_bounds) or (0 <= y + dy < height) and (0 <= x + dx < width)
        return horizontal_or_vertical and within_bounds

    neighbors = [(y + dy, x + dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if helper(x, dx, y, dy)]
    if include_self: neighbors.append(pos)
    return sorted(neighbors)

def deterministic_die():
    initial = 0
    while True:
        initial = initial % 100
        initial += 1
        yield initial + 1

def part1(input):
    p_1_pos = int(input[0].split(": ")[1])
    p_2_pos = int(input[1].split(": ")[1])
    
    cur_dice_number = 1
    cur_player = 1
    p_1_score = 0
    p_2_score = 0
    total_die_rolls = 0
    while p_1_score < 1000 and p_2_score < 1000:
        #print(p_1_score, p_2_score)
        next_numbers_sum= cur_dice_number*3 + 3
        cur_dice_number = cur_dice_number + 3 % 100
        total_die_rolls += 3
        if cur_player == 1:
            p_1_pos += next_numbers_sum
            p_1_pos = 1 + ((p_1_pos-1) % 10)
            p_1_score += p_1_pos
        else:
            p_2_pos += next_numbers_sum
            p_2_pos = 1 + ((p_2_pos-1) % 10)
            p_2_score += p_2_pos
        cur_player = 3 - cur_player
            
        
    answer = total_die_rolls * min(p_1_score,p_2_score)
    return answer


def part2(input):
    p_1_pos = int(input[0].split(": ")[1])
    p_2_pos = int(input[1].split(": ")[1])
    # hier product gebruiken en niet itertools.combinations_with_replacement :lol:
    all_possible_die_rolls = list(itertools.product((1,2,3),repeat=3))
    die_roll_counter = Counter(map(sum,all_possible_die_rolls))
    # lookup = {}
    needed_score = 21
    
    @lru_cache(maxsize=None)
    def calculate_win_count(p_1_pos, p_2_pos, p_1_score, p_2_score, cur_player):
        # if (p_1_pos, p_2_pos, p_1_score, p_2_score, cur_player) in lookup:
        #     return lookup[(p_1_pos, p_2_pos, p_1_score, p_2_score, cur_player)]
        num_wins_this_round = [0,0]
        og_players_pos = [p_1_pos, p_2_pos]
        og_players_score = [p_1_score, p_2_score]
        for sum_of_die_roll, num_occurrences in die_roll_counter.items():
            players_pos = copy.deepcopy(og_players_pos)
            players_score = copy.deepcopy(og_players_score)
            players_pos[cur_player] = (players_pos[cur_player] + sum_of_die_roll -1) %10 + 1
            players_score[cur_player] += players_pos[cur_player]
            if players_score[cur_player] >= needed_score:
                num_wins_this_round[cur_player] += num_occurrences
            else:
                wins_p1, wins_p2 = calculate_win_count(players_pos[0], players_pos[1], players_score[0], players_score[1], 1-cur_player)
                num_wins_this_round[0] += wins_p1 * num_occurrences
                num_wins_this_round[1] += wins_p2 * num_occurrences
        # lookup[(og_players_pos[0], og_players_pos[1], og_players_score[0], og_players_score[1], cur_player)] = tuple(num_wins_this_round)

        return num_wins_this_round[0], num_wins_this_round[1]

    player_1_wins, player_2_wins = calculate_win_count(p_1_pos, p_2_pos,0,0,0)
    answer = max(player_1_wins,player_2_wins)
    return answer


run_program("test_input.txt")
run_program("input.txt")
