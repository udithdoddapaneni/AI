import pycosat as ps
import math
import time

# test_sudoku = [ 
#     [0, 8, 0, 0, 9, 0, 2, 5, 4],
#     [0, 1, 0, 2, 0, 0, 0, 0, 0],
#     [0, 2, 0, 0, 6, 5, 9, 0, 0],
#     [0, 7, 1, 6, 0, 9, 0, 4, 0],
#     [3, 0, 0, 0, 0, 8, 0, 0, 6],
#     [0, 5, 6, 0, 0, 4, 0, 9, 0],
#     [0, 0, 0, 5, 8, 6, 0, 7, 0],
#     [5, 9, 0, 0, 0, 7, 1, 6, 2],
#     [0, 6, 4, 0, 1, 0, 5, 0, 8]
# ]

def precond(sudoku):
    """
    returns the state of the sudoku board as cnf of clauses
    """
    statements = []
    for i in range(len(sudoku)):
        for j in range(len(sudoku)):
            ele = sudoku[i][j]
            if ele == 0:
                continue
            statement = get_element_literals(i, j, len(sudoku))
            for k in range(len(statement)):
                z = statement[k]%len(sudoku)
                if z == 0:
                    z = len(sudoku)
                if z == ele:
                    statements.append([statement[k]])
                    continue
                else:
                    statements.append([-statement[k]])
    return statements

def get_element_literals(i, j, n):
    """
    returns the all the positive literals of a position in an n x n sudoku board
    """
    row = (n**2)*i + 1 # beginning element of row
    column = row + n*j # beginning element of the column of that row
    l = []
    for i in range(column, column+n):
        l.append(i)
    return l

def single_position_check(i, j, n):
    """
    returns the conditions that any position in a sudoku must satisfy
    returns as clauses in cnf form

    conditions:
    i) every position must have a number
    ii) one position must not have multiple numbers
    """
    literals = get_element_literals(i, j, n)
    statements = [literals]
    for i in range(n):
        for j in range(i+1, n):
            statements.append([-literals[i], -literals[j]])
    return statements

def single_row_check(i, n): # i: row number, n: size (nxn)
    """
    returns the conditions that ith given row in any sudoku of size nxn must satisfy
    returns as clauses in cnf form

    conditions:
    i) there should be no repeated number in a row
    """
    literalist= [] # precomputing
    for j in range(n):
        e = get_element_literals(i, j, n)
        literalist.append(e)
    statements = []
    for j1 in range(n):
        for j2 in range(j1+1, n):
            e1 = literalist[j1]
            e2 = literalist[j2]
            for k in range(n):
                statements.append([-e1[k], -e2[k]]) # (pixk & piyk) is not possible: so (~pixk) v (~piyk)
    return statements

def single_column_check(j, n):
    """
    returns the conditions that any jth column in any sudoku of size nxn must satisfy
    returns as clauses in cnf form

    conditions:
    i) there should be no repeated number in a column
    """
    literalist= [] # precomputing
    for i in range(n):
        e = get_element_literals(i, j, n)
        literalist.append(e)
    statements = []
    for i1 in range(n):
        for i2 in range(i1+1, n):
            e1 = literalist[i1]
            e2 = literalist[i2]
            for k in range(n):
                statements.append([-e1[k], -e2[k]]) # (pxjk & pyjk) is not possible: so (~pxjk) v (~pyjk)
    return statements

def get_block(i, j, n):
    """
    returns all the literals associated with the block having top left corner at (i,j) position
    """
    literalist = []
    N = int(math.sqrt(n))
    for x in range(i, i+N):
        for y in range(j, j+N):
            literalist.append(get_element_literals(x, y, n))
    return literalist

def single_block_check(i, j, n):
    """
    returns the conditions that any block having topleft corner at (i,j)th position in a sudoku of size nxn must satisfy
    returns as clauses in cnf form

    conditions:
    i) there should be no repeated number in a block
    """
    N = int(math.sqrt(n))
    literalist= get_block(i, j, n) # precomputing
    statements = []
    for i1 in range(len(literalist)):
        for i2 in range(i1+1, len(literalist)):
            e1 = literalist[i1]
            e2 = literalist[i2]
            for k in range(n):
                statements.append([-e1[k], -e2[k]])
    return statements

def position_check(n):
    """
    returns all the positional constraints that the board must satisfy
    returns as clauses in cnf form
    """
    statements = []
    for i in range(n):
        for j in range(n):
            statements += single_position_check(i, j, n)
    return statements

def row_check(n):
    """
    returns all the row constraints that the board must satisfy
    returns as clauses in cnf form
    """
    statements = []
    for i in range(n):
        statements += single_row_check(i, n)
    return statements

def column_check(n):
    """
    returns all the column constraints that the board must satisfy
    returns as clauses in cnf form
    """
    statements = []
    for j in range(n):
        statements += single_column_check(j, n)
    return statements

def block_check(n):
    """
    returns all the block constraints that the board must satisfy
    returns as clauses in cnf form
    """
    statements = []
    N = int(math.sqrt(n))
    for i in range(0, n, N):
        for j in range(0, n, N):
            statements += single_block_check(i, j, n)
    return statements

def total_check(sudoku):
    """
    checks whether the given board is following the necessary conditions
    if yes then it will return the all the literals and their boolean values (positive means true, negative means false)
    """
    n = len(sudoku)
    statements = block_check(n) + column_check(n) + row_check(n) + position_check(n) + precond(sudoku)
    ans = ps.solve(statements)
    return ans

def construct(solution_literals, n):
    """
    construct the sudoku board from the literals
    """
    ans = [[0]*n for i in range(n)]
    for literal in solution_literals:
        if literal <= 0:
            continue
        vali = literal-1
        i = vali//(n*n)
        valj = (literal-1)%(n*n)
        j = valj//n
        valk = valj%n
        k = valk+1
        ans[i][j] = k
    return ans


def solution(sudoku):
    """putting them all together"""
    n = len(sudoku)
    solution_literals = total_check(sudoku)
    if solution_literals == 'UNSAT':
        print('unsatisfiable')
        return 'UNSAT'
    matrix = construct(solution_literals, n)

    print("before:\n")
    for i in sudoku:
        print(*i)
    print("\n")

    print("after:\n")
    ans = ""
    for i in matrix:
        print(*i)
        ans += ''.join([str(j) for j in i])
    return ans

def conv_to_matrix(s: str):
    """converts the string into sudoku matrix form"""
    N = len(s)
    n = int(math.sqrt(N))
    matrix = [[0]*n for i in range(n)]
    for i in range(N):
        if s[i] == '.':
            continue
        ii = i//n
        jj = i%n
        matrix[ii][jj] = int(s[i])
    return matrix

def main():
    file = open("p.txt", "r")
    output = open("output.txt", "w")
    matrices = file.read().strip().split("\n")
    for i in range(len(matrices)):
        ans = solution(conv_to_matrix(matrices[i]))
        output.write(ans + "\n")
    file.close()
    output.close()

st = time.time()
main()
et = time.time()
print('')
print('time taken', et-st)
