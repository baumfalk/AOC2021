import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re
import copy

"0735"
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

def parse_packet_mode_4(bin_str):
    number_str = ""
    for index in range(0, len(bin_str), 5):
        block = bin_str[index:index + 5]
        if block[0] == "0":  # final block
            number_str += block[1:]
            bin_str=bin_str[(index + 5):]
            break
        else:
            number_str += block[1:]
    number = int(number_str, 2)
    return number, bin_str

def parse_packet(bin_str):
    og_length = len(bin_str)

    version = int(bin_str[:3],2)
    type = int(bin_str[3:6],2)
    rest = bin_str[6:]
    total_version = version
    if type == 4:
        num, rest = parse_packet_mode_4(rest)
        bytes_parsed = og_length - len(rest)
        #print(num, bytes_parsed, rest)
        return num, bytes_parsed, rest, total_version
    else:
        length_type = int(rest[0])
        rest = rest[1:]
        if length_type == 0:
            total_length_in_bits_of_subpackets = int(rest[:15],2)
            rest = rest[15:]
            length_remaining = total_length_in_bits_of_subpackets
            nums = []
            while length_remaining:
                num, bytes_parsed, rest,received_version = parse_packet(rest)
                total_version += received_version
                nums.append(num)
                length_remaining -= bytes_parsed
            bytes_parsed = og_length - len(rest)
            #print(nums, bytes_parsed, rest)

            #return nums, bytes_parsed, rest, total_version
        else:
            number_of_subpackets_in_packet = int(rest[:11],2)
            rest=rest[11:]
            num_packets_remaining = number_of_subpackets_in_packet
            nums = []
            for _ in range(num_packets_remaining):
                num, bytes_parsed, rest,received_version = parse_packet(rest)
                total_version += received_version
                nums.append(num)
            bytes_parsed = og_length - len(rest)
            #print(nums, bytes_parsed, rest)

            #return nums, bytes_parsed, rest, total_version
            pass
        
        if type == 0:
            return sum(nums),bytes_parsed, rest, total_version
        elif type == 1:
            return np.prod(nums),bytes_parsed, rest, total_version
        elif type==2:
            return min(nums),bytes_parsed, rest, total_version
        elif type==3:
            return max(nums),bytes_parsed, rest, total_version
        elif type==5:
            return int(nums[0] > nums[1]),bytes_parsed, rest, total_version
        elif type==6:
            return int(nums[0] < nums[1]),bytes_parsed, rest, total_version
        elif type==7:
            return int(nums[0] == nums[1]),bytes_parsed, rest, total_version
        print("ERROR")
        return nums, bytes_parsed, rest, total_version
        
    

def part1(input):
    # hex to binary
    num_in_hex = input[0]
    #hex_to_int = int(num_in_hex, 16)
    #binary = str(bin(hex_to_int))[2:]
    #number_of_zeros_missing = len(binary) % 4
    num_in_binary_str = ""
    replacement_dict = {"0" : "0000",
    "1" : "0001",
    "2" : "0010",
    "3" : "0011",
    "4" : "0100",
    "5" : "0101",
    "6" : "0110",
    "7" : "0111",
    "8" : "1000",
    "9" : "1001",
    "A" : "1010",
    "B" : "1011",
    "C" : "1100",
    "D" : "1101",
    "E" : "1110",
    "F" : "1111",}
    
    for digit in num_in_hex:
        bin_str = replacement_dict[digit]
        num_in_binary_str += bin_str
    binary = num_in_binary_str
    nums, bytes_parsed, rest, version_sum = parse_packet(binary)
    
    answer = version_sum
    return answer


def part2(input):
    # hex to binary
    num_in_hex = input[0]
    # hex_to_int = int(num_in_hex, 16)
    # binary = str(bin(hex_to_int))[2:]
    # number_of_zeros_missing = len(binary) % 4
    num_in_binary_str = ""
    replacement_dict = {"0": "0000",
                        "1": "0001",
                        "2": "0010",
                        "3": "0011",
                        "4": "0100",
                        "5": "0101",
                        "6": "0110",
                        "7": "0111",
                        "8": "1000",
                        "9": "1001",
                        "A": "1010",
                        "B": "1011",
                        "C": "1100",
                        "D": "1101",
                        "E": "1110",
                        "F": "1111", }

    for digit in num_in_hex:
        bin_str = replacement_dict[digit]
        num_in_binary_str += bin_str
    binary = num_in_binary_str
    nums, bytes_parsed, rest, version_sum = parse_packet(binary)

    answer = nums
    return answer


run_program("test_input.txt")
run_program("input.txt")
