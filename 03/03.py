import numpy as np
def run_program(inp="input.txt"):
    diag = np.genfromtxt(inp, delimiter=1).astype(int)
    content = list(map(lambda s: s.strip('\r\n'), open(inp).readlines()))
    print(part1(content))
    print(part2(content))
    print()
    
def part1(input):
    #instructions = [inp.split(" ") for inp in input]
    int_list = list(map(lambda x: list(map(int,list(x))),input))
    matrix = np.array(int_list)
    gamma = list(map(str,(np.sum(matrix, axis=0) > len(matrix)//2).astype(int)))
    gamma_str = "".join(gamma)
    epsilon = list(map(str,(np.sum(matrix, axis=0) < len(matrix)//2).astype(int)))
    epsilon_str = "".join(epsilon)
    #print(gamma_str, epsilon_str, int(gamma_str, 2), int(epsilon_str, 2))
    gamma = int(gamma_str, 2)
    eps = int(epsilon_str, 2)
    answer = gamma * eps
    return answer

def part2(input):
    #instructions = [inp.split(" ") for inp in input]
    #int_list = list(map(int,input))
    int_list = list(map(lambda x: list(map(int, list(x))), input))
    matrix = np.array(int_list)
    cur_matrix_oxygen = matrix.copy()
    cur_matrix_co2 = matrix.copy()

    for i in range(matrix.shape[1]):
        num_rows_oxygen = len(cur_matrix_oxygen)
        num_rows_co2= len(cur_matrix_oxygen)
        ox_num_ones_in_column = np.sum(cur_matrix_oxygen[:, i])
        if ox_num_ones_in_column > num_rows_oxygen/2:
            cur_matrix_oxygen = cur_matrix_oxygen[cur_matrix_oxygen[:,i] == 1]
        elif ox_num_ones_in_column == num_rows_oxygen/2:
            cur_matrix_oxygen = cur_matrix_oxygen[cur_matrix_oxygen[:, i] == 1]
        else:
            cur_matrix_oxygen = cur_matrix_oxygen[cur_matrix_oxygen[:, i] == 0]

    for i in range(matrix.shape[1]):
        num_rows_co2 = len(cur_matrix_co2)
        if num_rows_co2 == 1:
            break
        co2_num_ones_in_column = np.sum(cur_matrix_co2[:, i])
        if co2_num_ones_in_column > num_rows_co2/2:
            cur_matrix_co2 = cur_matrix_co2[cur_matrix_co2[:,i] == 0]
        elif co2_num_ones_in_column == num_rows_co2/2:
            cur_matrix_co2 = cur_matrix_co2[cur_matrix_co2[:, i] == 0]
        else:
            cur_matrix_co2 = cur_matrix_co2[cur_matrix_co2[:, i] == 1]
    oxygen = int("".join(list(map(str,list(cur_matrix_oxygen[0])))),2)
    co2 = int("".join(list(map(str,list(cur_matrix_co2[0])))),2)
    answer = oxygen*co2
    return answer

run_program("test_input.txt")
run_program("input.txt")
