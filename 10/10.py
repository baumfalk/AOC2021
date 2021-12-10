import numpy as np
from collections import defaultdict
from collections import Counter
import networkx as nx
import re

def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(f"Running on {inp}")
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    """
    ): 3 points.
]: 57 points.
}: 1197 points.
>: 25137 points.
    :param input: 
    :return: 
    """
    lookup={
        ")":3,
        "]":57,
        "}":1197,
        ">":25137
    }
    
    reverse={
        ")":"(",
        "]":"[",
        "}":"{",
        ">":"<"
    }
    
    total_score = 0
    for line in input:
        stack = []
        for char in line:
            char_is_closing_tag = char in lookup.keys()
            if char_is_closing_tag:
                opening_tag = reverse[char]
                if stack[-1] != opening_tag:
                    total_score +=  lookup[char]
                    break
                else:
                    stack = stack[:-1]
            else:
                stack.append(char)
                
    answer = total_score
    return answer

def part2(input):
    """
     ): 1 point.
]: 2 points.
}: 3 points.
>: 4 points. 
      """
    lookup = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    _reverse = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<"
    }
    rev_reverse = {val : key for key,val in _reverse.items()}

    total_scores = []
    complete_lines = []
    
    for line in input:
        stack = []
        complete = True
        for char in line:
            char_is_closing_tag = char in lookup.keys()
            if char_is_closing_tag:
                opening_tag = _reverse[char]
                if stack[-1] != opening_tag:
                    complete = False
                    #total_score += lookup[char]
                    break
                else:
                    stack = stack[:-1]
            else:
                stack.append(char)
        if complete:
            complete_lines.append((line, stack))
            score = 0
            for char in stack[::-1]:
                closing_tag = rev_reverse[char]
                score *= 5
                score += lookup[closing_tag]
            total_scores.append(score)
    total_scores = sorted(total_scores)
    answer = total_scores[len(total_scores)//2]
    return answer


run_program("test_input.txt")
run_program("input.txt")
