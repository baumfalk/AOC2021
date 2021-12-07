content = list(map(lambda s: s.strip('\r\n'), open("input.txt").readlines()))

def part1(input):
    int_list = list(map(int,input))
    teller = 0
    for index in range(len(int_list)-1):
        teller += int_list[index] < int_list[index+1]
    return teller

def part2(input):
    int_list = list(map(int,input))
    teller = 0
    for index in range(len(int_list)-3):
        teller += sum(int_list[index:(index+3)]) < sum(int_list[(index+1):(index+4)])
    return teller

print(part1(content))
print(part2(content))
