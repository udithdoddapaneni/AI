import numpy as np
import copy



LIMIT = 6

def count(s):
    o = 0
    x = 0
    y = 0
    z = 0
    c = 0
    p = 0
    q = 0
    r = 0
    for i in range(len(s)-3):
        P = s[i:i+4]
        if P == '1111':
            o += 1
        elif P == '1110' or P == '0111' or P == '1011' or P == '1101':
            x += 1
        elif P == '1100' or P == '0110' or P == '0011' or P == '1001' or P == '1010' or P == '0101':
            y += 1
        elif P == '1000' or P == '0100' or P == '0010' or P == '0001':
            z += 1
        elif P == '2222':
            c += 1
        elif P == '2220' or P == '0222' or P == '2022' or P == '2202':
            p += 1
        elif P == '2200' or P == '0220' or P == '0022' or P == '2002' or P == '2020' or P == '0202':
            q += 1
        elif P == '2000' or P == '0200' or P == '0020' or P == '0002':
            r += 1
            
    return o,x,y,z,c,p,q,r

def generate_moves(board, player_number): ## later try using yield instead of return
    for i in range(7):
        for j in range(5, -1, -1):
            if board[j][i] == 0:
                new_board = copy.deepcopy(board)
                new_board[j][i] = player_number
                yield new_board
                break


def change_player(player_number):
    if player_number == 1:
        return 2
    return 1

def evl(s: str, player_number):
    ai_value = 0
    enemy_value = 0
    o,x,y,z,c,p,q,r = count(s)
    if player_number == 1:

        if o > 0:
            return 1e9, 0
        ai_value += x*43*43
        ai_value += y*43
        ai_value += z

        # ai_prevention_score = (count(s, '2220') + count(s, '0222') + count(s, '2022') + count(s, '2202'))
        # enemy_prevention_score = count(s, )

        if c > 0:
            return 0, 1e9
        
        enemy_value += p*43*43
        enemy_value += q*43
        enemy_value += r

    else:

        if o > 0:
            return 0, 1e9
        enemy_value += x*43*43
        enemy_value += y*43
        enemy_value += z

        if c > 0:
            return 1e9, 0
        ai_value += p*43*43
        ai_value += q*43
        ai_value += r
    
    return ai_value, enemy_value

def expecti_min(state, limit, parent_val, ai_player, sign, player_number, depth):

    if sign*ai_player.evaluation_function(state) == -1e9:
        return -1e9+(43*43)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43*43)*depth
    if limit == LIMIT:
        avg = 0
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            avg += m
        return avg

    M = 1e9
    for i in generate_moves(state, player_number):
        m = expecti_max(i, limit+1, M, ai_player, -sign, change_player(player_number), depth+1)/7
        if m < M:
            M = m
        if M < parent_val:
            break

    return M

def min_move(state, limit, parent_val, ai_player, sign, player_number, depth):

    if sign*ai_player.evaluation_function(state) == -1e9:
        return -1e9+(43*43)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43*43)*depth
    if limit == LIMIT:
        M = 1e9
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            M = min(m, M)
        if M == -1e9:
            return M+(43*43)*(depth+1)
        if M == 1e9:
            return M-(43*43)*(depth+1)
        return M

    M = 1e9
    for i in generate_moves(state, player_number):
        m = max_move(i, limit+1, M, ai_player, -sign, change_player(player_number), depth+1)
        if m < M:
            M = m
        if M < parent_val:
            break

    return M

def expecti_max(state, limit, parent_val, ai_player, sign, player_number, depth):

    if sign*ai_player.evaluation_function(state) == -1e9:
        return -1e9+(43*43)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43*43)*depth
    
    if limit == LIMIT:
        avg = 0
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            avg += m
        return avg
    
    M = -1e9
    for i in generate_moves(state, player_number):
        m = expecti_min(i, limit+1, M, ai_player, -sign, change_player(player_number), depth+1)
        if m > M:
            M = m
        if M > parent_val:
            break

    return M

def max_move(state, limit, parent_val, ai_player, sign, player_number, depth):

    if sign*ai_player.evaluation_function(state) == -1e9:
        return -1e9+(43*43)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43*43)*depth
    
    if limit == LIMIT:
        M = -1e9
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            M = max(m, M)
        if M == -1e9:
            return M+(43*43)*(depth+1)
        if M == 1e9:
            return M-(43*43)*(depth+1)
        return M
    
    M = -1e9
    for i in generate_moves(state, player_number):
        m = min_move(i, limit+1, M, ai_player, -sign, change_player(player_number), depth+1)
        if m > M:
            M = m
        if M > parent_val:
            break

    return M

def print_state(state): # debugging
    for i in state:
        print(*i)

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        M = -1e10
        next_state = None
        parent_val = 0
        for state in generate_moves(board, self.player_number):
            if self.evaluation_function(state) == 1e9:
                next_state = state
                M = 1e9
                break
            m = min_move(state, 1, M, self, -1, change_player(self.player_number), 1)
            # print(m)
            # print_state(state)
            if m > M:
                M = m
                next_state = state

        for i in range(7):
            for j in range(5, -1, -1):
                if board[j][i] != next_state[j][i]:
                    return i
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        M = -1e10
        next_state = None
        parent_val = 0
        for state in generate_moves(board, self.player_number):
            if self.evaluation_function(state) == 1e9:
                next_state = state
                M = 1e9
                break
            m = expecti_min(state, 1, M, self, -1, change_player(self.player_number), 1)
            if m > M:
                M = m
                next_state = state

        for i in range(7):
            for j in range(5, -1, -1):
                if board[j][i] != next_state[j][i]:
                    return i
        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        ai_value = 0
        enemy_value = 0
        for row in np.row_stack(board):
            s = ''.join([str(i) for i in row])
            a,e = evl(s, self.player_number)
            if a == 1e9:
                return 1e9
            if e == 1e9:
                return -1e9
            ai_value += a; enemy_value += e

        for column in np.column_stack(board):
            s = ''.join([str(i) for i in column])
            a,e = evl(s, self.player_number)
            if a == 1e9:
                return 1e9
            if e == 1e9:
                return -1e9
            ai_value += a; enemy_value += e

        for i in range(-2, 3):

            s = ''.join([str(i) for i in np.diag(board, i)])
            a,e = evl(s, self.player_number)
            if a == 1e9:
                return 1e9
            if e == 1e9:
                return -1e9
            ai_value += a; enemy_value += e

            s = ''.join([str(i) for i in np.diag(np.rot90(board), i)])
            a,e = evl(s, self.player_number)
            if a == 1e9:
                return 1e9
            if e == 1e9:
                return -1e9
            ai_value += a; enemy_value += e
        
        # if ai_value == 1e9 and enemy_value == 1e9:
        #     print(board)
        if enemy_value == 1e9:
            return -enemy_value
        if ai_value == 1e9:
            return ai_value
    
        return ai_value-enemy_value

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
