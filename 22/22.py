from typing import List

import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy
import itertools
import scipy.sparse
from shapely.geometry import LineString

"0725"


def run_program(inp="input.txt"):
    # diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    # print(part1(content))
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


def parse_line(line):
    # on x=-20..26,y=-36..17,z=-47..7
    x_part, y_part, z_part = line.split(",")
    x_rest, x_right = x_part.split("..")
    x_rest, x_left = x_rest.split("=")
    x_min, x_max = min(int(x_right), int(x_left)), max(int(x_right), int(x_left))
    on_or_off = x_rest.split(" ")[0]
    y_rest, y_right = y_part.split("..")
    y_left = y_rest.split("=")[1]
    y_min, y_max = min(int(y_right), int(y_left)), max(int(y_right), int(y_left))

    z_rest, z_right = z_part.split("..")
    z_left = z_rest.split("=")[1]
    z_min, z_max = min(int(z_right), int(z_left)), max(int(z_right), int(z_left))

    return on_or_off, x_min, x_max, y_min, y_max, z_min, z_max


def part1(input):
    instructions = [parse_line(line) for line in input]
    grid = {}
    # offset=100000

    # grid_matrix = scipy.sparse.csr_matrix((offset*2, offset*2,offset*2))
    for on_or_off, x_min, x_max, y_min, y_max, z_min, z_max in instructions:
        # print(on_or_off, x_min,x_max, y_min, y_max, z_min, z_max)

        x_min = max(-50, x_min)
        x_max = min(50, x_max)
        y_min = max(-50, y_min)
        y_max = min(50, y_max)
        z_min = max(-50, z_min)
        z_max = min(50, z_max)
        # print("\t", on_or_off, x_min,x_max, y_min, y_max, z_min, z_max)
        if (x_min < -50 or x_max > 50) or (y_min < -50 or y_max > 50) or (z_min < -50 or z_max > 50):
            continue
        # grid_matrix = grid_matrix.tolil()[x_min:(x_max+1),y_min:(y_max+1), z_min:(z_max+1)] = 1 if on_or_off == "on" else 0
        # grid_matrix = grid_matrix.tocsr()
        # print("\t", on_or_off, x_min,x_max, y_min, y_max, z_min, z_max)
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    grid[(z, y, x)] = 1 if on_or_off == "on" else 0

    count_on = Counter(grid.values())
    answer = count_on[1]
    # answer = grid_matrix.sum()
    return answer


class Beam:
    def __init__(self, is_adding_beam, x_min, x_max, y_min, y_max, z_min, z_max):
        tpl = is_adding_beam, x_min, x_max, y_min, y_max, z_min, z_max
        self.is_adding_beam, self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max = tpl

    def __repr__(self):
        return f"Beam({self.is_adding_beam, self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max})"
    
    
    
    def __str__(self):
        def token(x):
            if x < self.x_min:
                return "."
            elif x > self.x_max:
                return "."
            else:
                return "+" if self.is_adding_beam else "-"
        return "".join([token(x) for x in range(0,4)])
    
    def fingerprint(self):
        return self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max

    def area(self):
        x_len = ((self.x_max + 1) - self.x_min)
        y_len = ((self.y_max + 1) - self.y_min)
        z_len = ((self.z_max + 1) - self.z_min)
        return x_len * y_len * z_len

    def get_lines(self):
        own_x_line = LineString([(self.x_min, 0), (self.x_max + 1, 0)])
        own_y_line = LineString([(self.y_min, 0), (self.y_max + 1, 0)])
        own_z_line = LineString([(self.z_min, 0), (self.z_max + 1, 0)])
        return own_x_line, own_y_line, own_z_line

    def overlap(self, other_cube):
        lines = self.get_lines()
        other_lines = other_cube.get_lines()

        if not all([line_1.intersects(line_2) for line_1, line_2 in zip(lines, other_lines)]):
            return None
        intersections = [line_1.intersection(line_2) for line_1, line_2 in zip(lines, other_lines)]
        positions = [pos for pair in
                     [(intersection.bounds[0], intersection.bounds[2] - 1) for intersection in intersections] for pos in
                     pair]
        is_adding_beam = None
        if self.is_adding_beam and other_cube.is_adding_beam:
            is_adding_beam = False
        elif self.is_adding_beam and not other_cube.is_adding_beam:
            is_adding_beam = False
        elif not self.is_adding_beam and other_cube.is_adding_beam:
            is_adding_beam = True
        elif not self.is_adding_beam and not other_cube.is_adding_beam:
            is_adding_beam = True
        assert is_adding_beam is not None
        return Beam(is_adding_beam, *positions)


class ListOfBeams:
    def __init__(self, list_of_beams):
        self.list_of_beams = list_of_beams

    def total_area(self):
        beam_area = Counter()
        for i in range(len(self.list_of_beams)):
            print(i,"/",len(self.list_of_beams))
            beam_1 = self.list_of_beams[i]
            # total_area += beam_1.area()
            new_beam_area = Counter()
            for old_beam, val in beam_area.items():
                old_beam = Beam(True, *old_beam)
                overlapping_beam = beam_1.overlap(old_beam)
                if overlapping_beam is not None:
                    new_beam_area[overlapping_beam.fingerprint()] -= val
            if beam_1.is_adding_beam:
                new_beam_area[beam_1.fingerprint()] += 1
            beam_area.update(new_beam_area)

        total_area = sum([Beam(True,*beam).area() * val for beam, val in beam_area.items()])
        # for index, beam in enumerate(self.list_of_beams):
        #     
        #     #if beam.is_adding_beam:
        #         #print(f"{'plus 'if index>0 else ''}{beam}",end=" ")
        #         #total_area += beam.area()
        #     if index == 0: continue
        #     for prev_index in range(index):
        #         prev_beam = self.list_of_beams[prev_index]
        #         prev_overlap_beam = dict_overlapping_cubes[beam.fingerprint()][prev_beam.fingerprint()]
        #         #print(prev_overlap_beam)
        #         if prev_overlap_beam.is_adding_beam:
        #             print("plus", prev_overlap_beam, end=" ")
        #             total_area += prev_overlap_beam.area()
        #         else:
        #             total_area -= prev_overlap_beam.area()
        #             print("minus", prev_overlap_beam, end=" ")
        # print()

        # for i in range(len(self.list_of_beams) - 1):
        #     beam_1 = self.list_of_beams[i]
        #     #total_area += beam_1.area()
        #     for j in range(i + 1, len(self.list_of_beams)):
        #         beam_2 = self.list_of_beams[j]
        #         overlapping_beam = beam_1.overlap(beam_2)
        #         if overlapping_beam:
        #             dict_overlapping_cubes[(beam_1.fingerprint(), beam_2.fingerprint())] = overlapping_beam
        #             #dict_overlapping_cubes[(beam_2.fingerprint(), beam_1.fingerprint())] = overlapping_beam
        #             # if overlapping_beam.is_adding_beam:
        #             #     total_area += overlapping_beam.area()
        #             # else:
        #             #     total_area -= overlapping_beam.area()

        return total_area


def part2(input):
    instructions = [parse_line(line) for line in input]
    beams = [(Beam(True if on_or_off == "on" else False, *args)) for on_or_off, *args in instructions]

    list_of_beams = ListOfBeams(beams)
    answer = list_of_beams.total_area()
    return answer


run_program("test_input.txt")
run_program("input.txt")
