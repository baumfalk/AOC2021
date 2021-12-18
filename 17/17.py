import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy

"0805"
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

def part1(input):
    "target area: x=20..30, y=-10..-5"
    left, right = input[0].split(", ")
    
    x_left, x_right = left.split("..")
    x_min = int(x_left.split("=")[1])
    x_max = int(x_right)

    y_left, y_right = right.split("..")
    y_max = int(y_right)
    y_min= int(y_left.split("=")[1])
    initial_x = 0
    initial_y = 0
    
    def max_x_val(vel_x):
        return np.sign(vel_x) * (abs(vel_x)**2 + abs(vel_x))/2
    
    def max_y_pos(vel_y):
        return (vel_y**2+vel_y)/2
    
    def x_pos_at_time_step(vel_x,t):
        return sum([max(0,vel_x - i) for i in range(t)])

    def min_x_needed_for_goal(x_goal_min):
        for vel_x in range(x_goal_min):
            if max_x_val(vel_x) >= x_goal_min:
                return vel_x
            
    def y_trajectory(vel_y, y_min, y_max):
        y_pos = 0
        trajectory = [y_pos]
        y_trajectory_within_bounds = []
        t = 0
        initial_vel_y = vel_y
        max_y_pos = 0
        while y_pos >= y_min:
            y_pos += vel_y
            if y_pos > max_y_pos:
                max_y_pos = y_pos
            vel_y -= 1
            trajectory.append(y_pos)
            if y_min <= y_pos <= y_max:
                y_trajectory_within_bounds.append((initial_vel_y,y_pos,max_y_pos,t))
            t += 1
        return trajectory, y_trajectory_within_bounds
    
    def suitable_trajectories(x_min, x_max, y_min, y_max):
        sensible_ys = []
        for y_vel in range(1,1000):
            y_traj, y_traj_within_bounds = y_trajectory(y_vel,y_min, y_max)
            if len(y_traj_within_bounds):
                sensible_ys += y_traj_within_bounds
       # print(sensible_ys)
        for vel_y, y_pos, max_y_pos,t in reversed(sensible_ys):
            min_x_needed = min_x_needed_for_goal(x_min)
            for x_vel in range(min_x_needed, 2*min_x_needed):
                x_pos = x_pos_at_time_step(x_vel, t)
                if x_min <= x_pos <= x_max:
                    return max_y_pos 

    answer = suitable_trajectories(x_min, x_max, y_min, y_max)   

    return answer


def part2(input):
    "target area: x=20..30, y=-10..-5"
    left, right = input[0].split(", ")

    x_left, x_right = left.split("..")
    x_min = int(x_left.split("=")[1])
    x_max = int(x_right)

    y_left, y_right = right.split("..")
    y_max = int(y_right)
    y_min = int(y_left.split("=")[1])
    initial_x = 0
    initial_y = 0

    def max_x_val(vel_x):
        return np.sign(vel_x) * (abs(vel_x) ** 2 + abs(vel_x)) / 2

    def max_y_pos(vel_y):
        return (vel_y ** 2 + vel_y) / 2

    def x_pos_at_time_step(vel_x, t):
        return sum([max(0, vel_x - i) for i in range(t)])

    def min_x_needed_for_goal(x_goal_min):
        for vel_x in range(x_goal_min):
            if max_x_val(vel_x) >= x_goal_min:
                return vel_x

    def y_trajectory(vel_y, y_min, y_max):
        y_pos = 0
        trajectory = [y_pos]
        y_trajectory_within_bounds = []
        t = 1
        initial_vel_y = vel_y
        max_y_pos = 0
        while y_pos >= y_min:
            y_pos += vel_y
            if y_pos > max_y_pos:
                max_y_pos = y_pos
            vel_y -= 1
            trajectory.append(y_pos)
            if y_min <= y_pos <= y_max:
                y_trajectory_within_bounds.append((initial_vel_y, y_pos, max_y_pos, t))
            t += 1
        return trajectory, y_trajectory_within_bounds

    def suitable_trajectories(x_min, x_max, y_min, y_max):
        sensible_ys = []
        for y_vel in range(-1000, 1000):
            y_traj, y_traj_within_bounds = y_trajectory(y_vel, y_min, y_max)
            if len(y_traj_within_bounds):
                sensible_ys += y_traj_within_bounds
        #print(sensible_ys)
        counter = 0
        for vel_y, y_pos, max_y_pos, t in reversed(sensible_ys):
            min_x_needed = min_x_needed_for_goal(x_min)
            for x_vel in range(min_x_needed, 2 * min_x_needed):
                x_pos = x_pos_at_time_step(x_vel, t)
                if x_min <= x_pos <= x_max:
                    counter += 1
        return counter

    #answer = suitable_trajectories(x_min, x_max, y_min, y_max)
    min_x_needed = min_x_needed_for_goal(x_min)
    counter = 0
    for y_vel in range(-100, 100):
        y_traj, y_traj_within_bounds = y_trajectory(y_vel, y_min, y_max)
        if len(y_traj_within_bounds):
            for x_vel in range(min_x_needed, min_x_needed*100):
                for vel_y, y_pos, max_y_pos, t in y_traj_within_bounds:
                    x_pos = x_pos_at_time_step(x_vel, t)
                    if x_min <= x_pos <= x_max:
                        #print(x_vel, y_vel)
                        counter += 1
                        break
    
    return counter


run_program("test_input.txt")
run_program("input.txt")
