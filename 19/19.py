from typing import List

import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy

def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).read().split("\n\n")))
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

def parse_scanner_info(scanner_info):
    relative_beacons = []
    rel_beacon_strings = scanner_info.split("\n")[1:]
    for rel_beacon_str in rel_beacon_strings:
        x,y,z = list(map(int, rel_beacon_str.split(",")))
        relative_beacons.append(np.array((x,y,z)))
        

    return relative_beacons

def calculate_relative_distances(relative_beacon_positions):
    distances = {}
    G = nx.Graph()
    for first_pos in relative_beacon_positions:
        first_pos = np.array(first_pos)
        first_pos_tpl =tuple(first_pos)

        for second_pos in relative_beacon_positions:
            second_pos = np.array(second_pos)
            second_pos_tpl = tuple(second_pos)

            if (first_pos_tpl == second_pos_tpl) or (second_pos_tpl,first_pos_tpl) in distances:
                continue
            distance = 13*np.sum((first_pos-second_pos)**2) + 11*np.sum(np.abs(first_pos-second_pos)) #+ 17*np.sum(np.abs(first_pos*second_pos))
            distance_per_unit = first_pos-second_pos
            G.add_edge(first_pos_tpl, second_pos_tpl, distance=distance, distance_per_unit=distance_per_unit)

            distances[(first_pos_tpl, second_pos_tpl)] = (distance, distance_per_unit)
            #distances[(second_pos_tpl, first_pos_tpl)] = distance
    return distances,G

def convert_pos_to_other_base(position, rotation, other_sensor_pos = None):
    x_pos_in_G_2_coord = position[rotation[0][0]] * rotation[0][1]
    y_pos_in_G_2_coord = position[rotation[1][0]] * rotation[1][1]
    z_pos_in_G_2_coord = position[rotation[2][0]] * rotation[2][1]
    
    if other_sensor_pos is None:
        return np.array([x_pos_in_G_2_coord, y_pos_in_G_2_coord, z_pos_in_G_2_coord])
    return other_sensor_pos + np.array([x_pos_in_G_2_coord, y_pos_in_G_2_coord, z_pos_in_G_2_coord])

def match_nodes(G_1, G_2, lookup_beacon=None, G_1_origin=np.array([0,0,0]), ):
    import networkx.algorithms.isomorphism as iso
    import itertools
    #https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
    # vind een paar dat matcht
    edges_G_1 = nx.get_edge_attributes(G_1,"distance")
    edges_G_2 = nx.get_edge_attributes(G_2, "distance")
    edges_G_1_counter = Counter(edges_G_1.values())
    edges_G_2_counter = Counter(edges_G_2.values())
    both_distances = edges_G_1_counter.keys() & edges_G_2_counter.keys()
    relevant_edges_G_1 = {key for key, val in edges_G_1.items() if val in both_distances}
    relevant_edges_G_2 = {key for key, val in edges_G_2.items() if val in both_distances}
    relevant_nodes_G_1 = {frm for frm,_ in relevant_edges_G_1} | {to for _, to in relevant_edges_G_1} 
    relevant_nodes_G_2 = {frm for frm, _ in relevant_edges_G_2} | {to for _, to in relevant_edges_G_2}
    
    if len(relevant_nodes_G_1) < 12 or len(relevant_nodes_G_2) < 12:
        return None, None
    
    G_1_subgraph = G_1.subgraph(relevant_nodes_G_1)
    G_2_subgraph = G_2.subgraph(relevant_nodes_G_2)
    em = iso.numerical_edge_match("distance", 1)
    gm = iso.GraphMatcher(G_1_subgraph, G_2_subgraph, edge_match=em)
    mapping = None
    
    for subgraph_mapping in gm.isomorphisms_iter():
        mapping = subgraph_mapping
    if mapping is None:
        return None, None
        
    # we hebben een mapping, maar o jee hij is mogelijk nog geroteerd! Hoe komen we daar achter? 
    # pak twee nodes uit elke subgraph
    G_1_test_node_1, G_1_test_node_2 = list(G_1_subgraph.nodes)[:2]
    G_2_test_node_1, G_2_test_node_2 = mapping[G_1_test_node_1], mapping[G_1_test_node_2]
    
    edge_G_1_distances = G_1_subgraph[G_1_test_node_1][G_1_test_node_2]["distance_per_unit"]
    edge_G_2_distances = G_2_subgraph[G_2_test_node_1][G_2_test_node_2]["distance_per_unit"]

    
    rotation = compute_rotation_and_mirroring(G_1_test_node_1, G_1_test_node_2, G_2_test_node_1, G_2_test_node_2)
    
        
    #rotation = compute_rotation(edge_G_1_distances, edge_G_2_distances)
    
    G_2_test_node_1_in_G_1_pos_displaced = convert_pos_to_other_base(G_2_test_node_1, rotation)
    G_2_sensor_pos_in_G_1_base = determine_sensor_pos_in_other_system(G_2_test_node_1_in_G_1_pos_displaced, G_1_test_node_1)
    
    G_2_test_node_1_in_G_1_pos_complete = convert_pos_to_other_base(G_2_test_node_1, rotation, G_2_sensor_pos_in_G_1_base)

    #G_2_position
    return G_2_sensor_pos_in_G_1_base, rotation

def determine_sensor_pos_in_other_system(displaced_node_in_other_system, equivalent_node_in_normal_system):
        return equivalent_node_in_normal_system - displaced_node_in_other_system

def compute_rotation(distances_per_axis_system_1, distances_per_axis_system_2):
    rotation = {}
    for left in range(3):
        for right in range(3):
            if distances_per_axis_system_1[left] == distances_per_axis_system_2[right]:
                rotation[left] = (right, 1)
            elif distances_per_axis_system_1[left] == distances_per_axis_system_2[right] * -1:
                rotation[left] = (right, -1)
    return rotation

def compute_rotation_and_mirroring(G_1_test_node_1,G_1_test_node_2,G_2_test_node_1,G_2_test_node_2):
    G_1_test_node_1 = np.array(G_1_test_node_1)
    G_1_test_node_2 = np.array(G_1_test_node_2)
    G_2_test_node_1 = np.array(G_2_test_node_1)
    G_2_test_node_2 = np.array(G_2_test_node_2)
    distances_per_axis_system_1 = G_1_test_node_1 - G_1_test_node_2
    distances_per_axis_system_2 = G_2_test_node_1 - G_2_test_node_2
    rotation = {}
    for left in range(3):
        for right in range(3):
            if distances_per_axis_system_1[left] == distances_per_axis_system_2[right]:
                rotation[left] = (right, 1)
                break
            elif distances_per_axis_system_1[left] == distances_per_axis_system_2[right] * -1:
                rotation[left] = (right,-1)
                break
   
    return rotation

def part1(input):
    max_distance = 1000
    relative_beacon_positions_per_sensor = []
    all_distances_between_beacons = []
    all_beacon_graphs = []
    for scanner_info in input:
        beacon_locs = parse_scanner_info(scanner_info)
        relative_beacon_positions_per_sensor.append(beacon_locs)
        distances_between_beacons,G = calculate_relative_distances(beacon_locs)
        all_beacon_graphs.append(G)
        all_distances_between_beacons.append(distances_between_beacons)
    
    
    mapping_to_G_0 = dict()
    mapping_G_2_to_G_1 = dict()
    sensor_positions_base_0 = {0:(0,0,0)}
    G_0 = all_beacon_graphs[0]
    G_0_smoezelig = copy.deepcopy(all_beacon_graphs[0])

    all_beacons_set = set(G_0.nodes)
    converted_graphs = {}
    graphs_to_convert = [(i+1,G) for i,G in enumerate(all_beacon_graphs[1:])]
    for i in range(len(all_beacon_graphs)-1):
        G_1 = all_beacon_graphs[i]
        for j in range(i+1, len(all_beacon_graphs)):
            if (i,j) in mapping_G_2_to_G_1: continue
            G_2 = all_beacon_graphs[j]
            sensor_pos, rotation = match_nodes(G_1, G_2)
            if sensor_pos is not None:
                mapping_G_2_to_G_1[(i,j)] = sensor_pos, rotation
                #print(i,j," match ")
            sensor_pos, rotation = match_nodes(G_2, G_1)
            if sensor_pos is not None:
                mapping_G_2_to_G_1[(j, i)] = sensor_pos, rotation
                #print("\t",j, i, " match ")
    conversion_graph = nx.Graph()
    
    for frm, to in mapping_G_2_to_G_1:
        conversion_graph.add_edge(frm, to)
    
    nodes_in_base_0 = set(G_0.nodes)
    for i in range(1, len(all_beacon_graphs)):
        graph_to_convert = all_beacon_graphs[i]
        nodes_to_convert = graph_to_convert.nodes
        conversion_path = nx.shortest_path(conversion_graph, 0, i)
        conversion_order = list(reversed(list(zip(conversion_path[:-1], conversion_path[1:]))))
        print(f"Shortest path from 0 to {i}: {conversion_path}")
           
        prev_sensor_pos = None
        for to,frm in conversion_order:
            sensor_pos, rotation = mapping_G_2_to_G_1[(to, frm)]
            nodes_to_convert = [tuple(convert_pos_to_other_base(node, rotation, sensor_pos)) for node in nodes_to_convert]
            if prev_sensor_pos is None:
                prev_sensor_pos= sensor_pos
            else:
                prev_sensor_pos = convert_pos_to_other_base(prev_sensor_pos, rotation, sensor_pos)
        sensor_positions_base_0[i] = prev_sensor_pos
        nodes_in_base_0.update(nodes_to_convert)
    #print(sensor_positions_base_0)
    # while len(graphs_to_convert):        
    #     j, G_2 = graphs_to_convert.pop(0)
    #     print(j, end="")
    #     #print(f"trying to find mapping for scanner {j}" , end=": ")
    #     sensor_pos, rotation = match_nodes(G_0, G_2)
    #     if sensor_pos is None:
    #         for i in mapping_to_G_0:
    #             G_1 = all_beacon_graphs[i]
    #             sensor_pos_other_system, rotation_other_system = match_nodes(G_1, G_2)
    #             if sensor_pos_other_system is not None:
    #                 print(f"(matched with system {i})",end=" ")
    #         #print("no mapping found")
    #         graphs_to_convert.append((j,G_2))
    #         print()
    #         continue
    #     print("found")
    #     #print(f"mapping found! {sensor_pos, rotation}")
    #     mapping_to_G_0[j] = (sensor_pos, rotation)
    #     beacons_found_by_sensor = {node: tuple(convert_pos_to_other_base(node, rotation, sensor_pos)) for node in G_2}
    #     
    #     for from_node in G_2:
    #         from_node_translated = beacons_found_by_sensor[from_node]
    #         for to_node in G_2[from_node]:
    #             to_node_translated = beacons_found_by_sensor[to_node]
    #             attributes = G_2[from_node][to_node]
    #             G_0.add_edge(from_node_translated, to_node_translated)
    #     _, G_0 = calculate_relative_distances(G_0.nodes)
    #     all_beacons_set |= set(beacons_found_by_sensor.values())
                
    # answer = len(all_beacons_set)
    answer= len(nodes_in_base_0)
    max_dist= 0
    for sensor_1 in sensor_positions_base_0:
        pos_1 = np.array(sensor_positions_base_0[sensor_1])
        for sensor_2 in sensor_positions_base_0:
            pos_2 = np.array(sensor_positions_base_0[sensor_2])
            max_dist = max(np.sum(np.abs(pos_1 - pos_2)), max_dist)
    return answer, max_dist


def part2(input):
    answer = None
    return answer


run_program("test_input.txt")
run_program("input.txt")
 