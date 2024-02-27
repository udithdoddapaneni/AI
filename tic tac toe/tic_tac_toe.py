# tic tac toe
import sys
import copy

board = [['-']*3 for i in range(3)]


def check_rows(board: list[list[str]]) -> str:
    for i in board:
        if i == ['x','x','x']:
            return 'x'
        elif i == ['o','o','o']:
            return 'o'
    
    return '-'

def check_columns(board: list[list[str]]) -> str:
    for i in range(3):
        countx = 0
        counto = 0
        for j in range(3):
            if board[j][i] == 'x':
                countx += 1
            elif board[j][i] == 'o':
                counto += 1
        if countx == 3:
            return 'x'
        elif counto == 3:
            return 'o'
    
    return '-'

def check_diagonals(board: list[list[str]]) -> str:
    diagonal1 = [board[0][0], board[1][1], board[2][2]]
    diagonal2 = [board[0][2], board[1][1], board[2][0]]
    if diagonal1 == ['x','x','x'] or diagonal2 == ['x','x','x']:
        return 'x'
    if diagonal1 == ['o','o','o'] or diagonal2 == ['o','o','o']:
        return 'o'
    
    return '-'

def check_winner(board: list[list[str]]) -> str:
    x = check_rows(board)
    if x != '-':
        return x
    x = check_columns(board)
    #print(x)
    if x != '-':
        return x
    x = check_diagonals(board)
    if x != '-':
        return x
    return '-'

# player x
# ai o

def make_move_player(board: list[list[str]]):

    try:
        mover, movec = list(map(int, input('please make a move: ').split()))
        if board[mover][movec] != '-':
            raise ValueError
        board[mover][movec] = 'x'
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)
        print('invalid move. try again')
        make_move_player(board)

def possible_states(state: list[list[str]], c: str) -> list:
    
    states = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == '-':
                new_state = copy.deepcopy(state)
                new_state[i][j] = c
                states.append(new_state)
    
    return states

def utility(state: list[list[str]]) -> int: # ai uses this to minimize
    z = check_winner(state)
    if z == 'x':
        return 1
    elif z == 'o':
        return -1
    filled = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != '-':
                filled += 1
    if filled == 9:
        return 0
    x = 1
    for i in possible_states(state, 'o'):
        x = min(maximize(i), x)
        if x == -1:
            return -1
    return x

def maximize(state: list[list[str]]) -> int: # optimal play by player
    z = check_winner(state)
    if z == 'x':
        return 1
    elif z == 'o':
        return -1
    filled = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != '-':
                filled += 1
    if filled == 9:
        return 0
    x = -1
    for i in possible_states(state, 'x'):
        x = max(utility(i), x)
        if x == 1:
            return 1

    return x
    

def make_move_ai(state: list[list[str]]):

    x = 1
    new_state = None
    for i in possible_states(state, 'o'):
        y = maximize(i)
        if y <= x:
            new_state = i
            x = y
        if y == -1:
            for m in range(3):
                for n in range(3):
                    state[m][n] = i[m][n]
            return

    for m in range(3):
        for n in range(3):
            state[m][n] = new_state[m][n]
    
# game

def print_board():
    for i in board:
        print(' '.join(i))

turn = 'x' # player starts first
while True:

    print_board()
    if turn == 'x':
        make_move_player(board)
        turn = 'o'
    elif turn == 'o':
        print('ai move:')
        make_move_ai(board)
        turn = 'x'
    z = check_winner(board)
    if z == 'x':
        print_board()
        print('player wins')
        break
    elif z == 'o':
        print_board()
        print('ai wins')
        break
    filled = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                filled += 1
    if filled == 9:
        print_board()
        print('draw')
        break