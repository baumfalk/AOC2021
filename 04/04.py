import numpy as np
def run_program(inp="input.txt"):
    #diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    first_line = input[0]
    
    numbers_to_be_called = list(map(int,first_line.split(",")))
    
    rest_of_input = input[1:]
    
    list_of_fields = []
    
    for line in rest_of_input:
        if line == "":
            list_of_fields.append([])
            continue
        line = line.replace("  "," ")
        line = line.strip()
        list_of_fields[-1].append(line.split(" "))
    
    list_of_field_array = []
    list_of_bingos = []
    for i, field_str in enumerate(list_of_fields):
        list_of_field_array.append(np.array(field_str,dtype=int))
        list_of_bingos.append(np.zeros((5,5)))
    
    
    for number in numbers_to_be_called:
        for index, field in enumerate(list_of_field_array):
            
            
            y,x = np.where(field == number)
            bingo_field = list_of_bingos[index]
            bingo_field[y, x] = 1
            field[y,x] = 0 #TODO dit is link
            # check if winner
            #print(np.sum(bingo_field,axis=0))
            #print(np.sum(bingo_field,axis=1))
            winner_one = np.where(np.sum(bingo_field,axis=0) == 5)
            winner_two = np.where(np.sum(bingo_field,axis=1) == 5)
            if len(winner_one[0]) or len(winner_two[0]):
                answer = np.sum(field) * number
                return answer
    #int_list = list(map(int,input))

    #instructions = [inp.split(" ") for inp in input]
    #int_list = list(map(lambda x: list(map(int,list(x))),input))
    answer = None
    return answer

def part2(input):
    first_line = input[0]

    numbers_to_be_called = list(map(int, first_line.split(",")))

    rest_of_input = input[1:]

    list_of_fields = []

    for line in rest_of_input:
        if line == "":
            list_of_fields.append([])
            continue
        line = line.replace("  ", " ")
        line = line.strip()
        list_of_fields[-1].append(line.split(" "))

    list_of_field_array = []
    list_of_bingos = []
    for i, field_str in enumerate(list_of_fields):
        list_of_field_array.append(np.array(field_str, dtype=int))
        list_of_bingos.append(np.zeros((5, 5)))

    new_list_of_field_array = []
    new_list_of_bingos = []
    for number in numbers_to_be_called:
        new_list_of_field_array = []
        new_list_of_bingos = []
        for index, field in enumerate(list_of_field_array):

            y, x = np.where(field == number)
            bingo_field = list_of_bingos[index]
            bingo_field[y, x] = 1
            field[y, x] = 0  # TODO dit is link
            # check if winner
            # print(np.sum(bingo_field,axis=0))
            # print(np.sum(bingo_field,axis=1))
            winner_one = np.where(np.sum(bingo_field, axis=0) == 5)
            winner_two = np.where(np.sum(bingo_field, axis=1) == 5)
            if len(winner_one[0]) or len(winner_two[0]):
                if len(list_of_field_array) == 1:
                    answer = np.sum(field) * number
                    return answer
                continue
            new_list_of_field_array.append(field)
            new_list_of_bingos.append(bingo_field)
        list_of_field_array = new_list_of_field_array
        list_of_bingos = new_list_of_bingos
        
    # int_list = list(map(int,input))

    # instructions = [inp.split(" ") for inp in input]
    # int_list = list(map(lambda x: list(map(int,list(x))),input))
    answer = None
    return answer

run_program("test_input.txt")
run_program("input.txt")
