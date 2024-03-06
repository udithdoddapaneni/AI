import numpy as np
import copy



LIMIT = 4
def generate_moves(board, player_number): ## later try using yield instead of return
    moves = []
    for i in range(7):
        for j in range(5, -1, -1):
            if board[j][i] == 0:
                new_board = copy.deepcopy(board)
                new_board[j][i] = player_number
                moves.append(new_board)
                break

    return moves

def change_player(player_number):
    if player_number == 1:
        return 2
    return 1

def evl(s: str, player_number):
    ai_value = 0
    enemy_value = 0
    if player_number == 1:
        o = s.count('1111')
        x = (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))
        y = (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))
        z = (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

        if o > 0:
            return 1e9, 0
        ai_value += x*43**2
        ai_value += y*43
        ai_value += z

        c = s.count('2222')
        p = (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))
        q = (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))
        r = (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))

        # ai_prevention_score = (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))
        # enemy_prevention_score = s.count()

        if c > 0:
            return 0, 1e9
        enemy_value += p*43**2
        enemy_value += q*43
        enemy_value += r

    else:
        o = s.count('1111')
        x = (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))
        y = (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))
        z = (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

        if o > 0:
            return 0, 1e9
        enemy_value += x*43**2
        enemy_value += y*43
        enemy_value += z

        c = s.count('2222')
        p = (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))
        q = (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))
        r = (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))

        if c > 0:
            return 1e9, 0
        ai_value += p*43**2
        ai_value += q*43
        ai_value += r
    
    return ai_value, enemy_value

def expecti_min(state, limit, parent_val, ai_player, sign, player_number, depth):

    if sign*ai_player.evaluation_function(state) == -1e9:
        return -1e9+(43**2)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43**2)*depth
    if limit == LIMIT:
        avg = 0
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            avg += m/6
        return avg

    M = 1e9
    for i in generate_moves(state, player_number):
        m = expecti_max(i, limit+1, M, ai_player, -sign, change_player(player_number), depth+1)
        if m < M:
            M = m
        if M < parent_val:
            break

    return M

def min_move(state, limit, parent_val, ai_player, sign, player_number, depth):

    if sign*ai_player.evaluation_function(state) == -1e9:
        return -1e9+(43**2)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43**2)*depth
    if limit == LIMIT:
        M = 1e9
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            M = min(m, M)
        if M == -1e9:
            return M+(43**2)*(depth+1)
        if M == 1e9:
            return M-(43**2)*(depth+1)
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
        return -1e9+(43**2)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43**2)*depth
    
    if limit == LIMIT:
        avg = 0
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            avg += m/6
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
        return -1e9+(43**2)*depth
    if sign*ai_player.evaluation_function(state) == 1e9:
        return 1e9-(43**2)*depth
    
    if limit == LIMIT:
        M = -1e9
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            M = max(m, M)
        if M == -1e9:
            return M+(43**2)*(depth+1)
        if M == 1e9:
            return M-(43**2)*(depth+1)
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
