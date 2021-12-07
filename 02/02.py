content = list(map(lambda s: s.strip('\r\n'), open("input.txt").readlines()))

def part1(input):
    instructions = [inp.split(" ") for inp in input]
    
    ops = {
        "forward": (1,0),
        "down": (0,1),
        "up": (0,-1)
    }
    
    hor = 0
    depth = 0
    for op, amount in instructions:
        amount = int(amount)
        op_hor, op_depth = ops[op]
        hor += op_hor*amount
        depth += op_depth * amount
    
    return hor*depth

def part2(input):
    instructions = [inp.split(" ") for inp in input]

    ops = {
        "forward": (1, 0, 0, 1),
        "down": (0, 0, 1, 0),
        "up": (0, 0, -1, 0)
    }
    hor = 0
    depth = 0
    aim=0
    for op, amount in instructions:
        amount = int(amount)
        op_hor, op_depth, op_aim, op_aim_usage = ops[op]
        hor += op_hor * amount
        depth += op_depth * amount
        depth += aim * amount * op_aim_usage
        aim += op_aim*amount
    return hor * depth


print(part1(content))
print(part2(content))
