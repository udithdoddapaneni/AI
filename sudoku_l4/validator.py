'''
This module is used to validate the output data.
Follows these conditions:
    1. Each cell in puzzle contains at least one value.
    2. Each cell in the puzzle contains at most one value.
    3. Each row in the puzzle should contain all the values.
    4. Each column in the puzzle should contain all the values.
    5. Each smaller block should contain all the values.
    6. The initial setup (values for some of the cells).
'''

'''
    Input format: 
    ............8.5.492...6.3.1..9..........21.38...3.......5........6..48..13...96.2
    Output format:
    951243786673815249248967351389756124567421938412398567895672413726134895134589672
'''
def convert_input_to_puzzle(input_data):
    puzzle = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(input_data[i*9 + j])
        puzzle.append(row)
    return puzzle


def single_value_in_cell(puzzle):
    for i in range(9):
        for j in range(9):
            if len(puzzle[i][j]) != 1:
                return False
    return True

def at_most_one_value_in_cell(puzzle):
    for i in range(9):
        for j in range(9):
            if len(puzzle[i][j]) > 1:
                return False
    return True

def all_values_in_row(puzzle):
    for i in range(9):
        row = puzzle[i]
        row_values = set()
        for j in range(9):
            row_values.add(row[j])
        if len(row_values) != 9:
            return False
    return True

def all_values_in_column(puzzle):
    for i in range(9):
        column_values = set()
        for j in range(9):
            column_values.add(puzzle[j][i])
        if len(column_values) != 9:
            return False
    return True

def all_values_in_block(puzzle):
    for i in range(3):
        for j in range(3):
            block_values = set()
            for k in range(3):
                for l in range(3):
                    block_values.add(puzzle[i*3+k][j*3+l])
            if len(block_values) != 9:
                return False
    return True

def validate_puzzle(puzzle):
    if not single_value_in_cell(puzzle):
        return False
    if not at_most_one_value_in_cell(puzzle):
        return False
    if not all_values_in_row(puzzle):
        return False
    if not all_values_in_column(puzzle):
        return False
    if not all_values_in_block(puzzle):
        return False
    return True


# print(validate_puzzle("951243786673815249248967351389756124567421938412398567895672413726134895134589672"))
input_data = "951243786673815249244967351389756124567421938412398567895672413726134895134589672"
puzzle = convert_input_to_puzzle(input_data)
print(validate_puzzle(puzzle))
