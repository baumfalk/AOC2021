import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy

"0801"
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()
    
def neighbors_of_cell(pos, height, width):
    y,x = pos
    # (dy == dx == 0) and (dy != 0 and dx != 0)
    def helper(x, dx, y, dy):
        horizontal_or_vertical = not (dy != 0 and dx != 0) and not (dy == 0 and dx==0)
        within_bounds = (0 <= y + dy < height) and (0 <= x + dx < width)
        return horizontal_or_vertical and within_bounds
    neighbors = {(y+dy,x+dx) for dy in [-1,0,1] for dx in [-1,0,1] if helper(x, dx, y, dy)}
    return neighbors

def part1(input):
    grid = np.genfromtxt(input, delimiter=1).astype(int)
    height, width = grid.shape
    G = nx.DiGraph()
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            pos = y,x
            neighbors_indices = neighbors_of_cell(pos, height, width)
            for n_y,n_x in neighbors_indices:
                neighbor_val = grid[n_y,n_x]
                G.add_edge((y,x), (n_y,n_x), weight = neighbor_val)
    start_pos = (0,0)
    end_pos = (height-1, width-1)
    shortest_path = nx.shortest_path(G, start_pos, end_pos, "weight")
    shortest_path = shortest_path[1:]
    total_weight = sum(grid[y,x] for y,x in shortest_path)
    answer = total_weight
    return answer

def extend_grid(grid):
    temp_grid = grid - 1
    extra_grids = [((temp_grid + i) % 9) + 1 for i in range(1,5)]
    new_grid = grid.copy()
    
    for extra_grid in extra_grids:
        new_grid = np.concatenate((new_grid, extra_grid))
    new_grid_to_copy = new_grid.copy()
    for i in range(1,5):
        concat_grid = ((((new_grid_to_copy - 1) + i) % 9) + 1)
        new_grid = np.concatenate((new_grid, concat_grid), axis=1) 
        
    return new_grid


def extend_grid2(grid):
    og_grid = grid.copy()
    for i in range(1,5):
        addendum = og_grid+i
        addendum[addendum>9] = addendum[addendum>9] - 9

        grid = np.concatenate((grid, addendum))
    og_grid = grid.copy()
    for i in range(1,5):
        addendum = og_grid+i
        addendum[addendum>9] = addendum[addendum>9] - 9

        grid = np.concatenate((grid, addendum), axis=1)
   
    return grid

def part2(input):
    
    grid = np.genfromtxt(input, delimiter=1).astype(int)
    
    grid = extend_grid(grid)
    grid = extend_grid2(np.genfromtxt(input, delimiter=1).astype(int))
    height, width = grid.shape
    G = nx.DiGraph()
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            pos = y,x
            neighbors_indices = neighbors_of_cell(pos, height, width)
            for n_y,n_x in neighbors_indices:
                neighbor_val = grid[n_y,n_x]
                G.add_edge((y,x), (n_y,n_x), weight = neighbor_val)
    start_pos = (0,0)
    end_pos = (height-1, width-1)
    shortest_path = nx.shortest_path(G, start_pos, end_pos, "weight")
    shortest_path = shortest_path[1:]
    total_weight = sum(grid[y,x] for y,x in shortest_path)
    answer = total_weight
    return answer


run_program("test_input.txt")
run_program("input.txt")
