import numpy as np
import copy

LIMIT = 5

board = np.zeros([6,7]).astype(np.uint8)


board[5][0] = 2
board[5][1] = 2
board[5][2] = 2
board[5][3] = 1

board[4][3] = 1
board[3][3] = 1


def generate_moves(board, player_number): ## later try using yield instead of return
    moves = []
    # print(len(board), len(board[0]))
    for i in range(7):
        for j in range(5, -1, -1):
            new_board = copy.deepcopy(board)
            if new_board[j][i] == 0:
                new_board[j][i] = player_number
                moves.append(new_board)
                break

    return moves

def change_player(player_number):
    if player_number == 1:
        return 2
    return 1

def min_move(state, limit, parent_val, ai_player, sign, player_number):
    if limit == LIMIT:
        M = 1e9
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            M = min(m, M)
        return M
    
    M = 1e9
    for i in generate_moves(state, player_number):
        m = max_move(i, limit+1, M, ai_player, -sign, change_player(player_number))
        if m < M:
            M = m
        if M < parent_val:
            break
    
    return M

def max_move(state, limit, parent_val, ai_player, sign, player_number):
    if limit == LIMIT:
        M = -1e9
        for i in generate_moves(state, player_number):
            m = sign*ai_player.evaluation_function(i)
            M = max(m, M)
        return M
    
    M = -1e9
    for i in generate_moves(state, player_number):
        m = min_move(i, limit+1, M, ai_player, -sign, change_player(player_number))
        if m > M:
            M = m
        if M > parent_val:
            break

    return M

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        M = -1e9
        next_state = None
        parent_val = 0
        for state in generate_moves(board, self.player_number):
            m = min_move(state, 1, M, self, -1, change_player(self.player_number))
            print(state, m)
            if m >= M:
                M = m
                next_state = state
            # if M > parent_val:
            #     break
        print(next_state)
        for i in range(7):
            for j in range(5, -1, -1):
                if board[j][i] != next_state[j][i]:
                    return i
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):

        raise NotImplementedError('Whoops I don\'t know what to do')

    def evaluation_function(self, board):
        # checking rows
        ai_value = 0
        for row in np.row_stack(board):
            s = ''.join([str(i) for i in row])
            if self.player_number == 1:
                if s.count('1111') > 0:
                    return 1e9
                if s.count('2222') > 0:
                    return -1e9
                ai_value += (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value += (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value += (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value -= (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value -= (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value -= (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))
            else:
                if s.count('1111') > 0:
                    return -1e9
                if s.count('2222') > 0:
                    return 1e9
                ai_value -= (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value -= (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value -= (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value += (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value += (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value += (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))

        for column in np.column_stack(board):
            s = ''.join([str(i) for i in column])
            if self.player_number == 1:
                if s.count('1111') > 0:
                    return 1e9
                if s.count('2222') > 0:
                    return -1e9
                ai_value += (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value += (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value += (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value -= (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value -= (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value -= (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))
            
            else:
                if s.count('1111') > 0:
                    return -1e9
                if s.count('2222') > 0:
                    return 1e9
                ai_value -= (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value -= (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value -= (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value += (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value += (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value += (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))

        for i in range(-3, 3):

            s = ''.join([str(i) for i in np.diag(board, i)])
            if self.player_number == 1:
                if s.count('1111') > 0:
                    return 1e9
                if s.count('2222') > 0:
                    return -1e9
                ai_value += (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value += (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value += (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value -= (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value -= (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value -= (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))
            
            else:
                if s.count('1111') > 0:
                    return -1e9
                if s.count('2222') > 0:
                    return 1e9
                ai_value -= (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value -= (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value -= (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value += (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value += (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value += (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))
            s = ''.join([str(i) for i in np.diag(np.rot90(board), i)])
            if self.player_number == 1:
                if s.count('1111') > 0:
                    return 1e9
                if s.count('2222') > 0:
                    return -1e9
                ai_value += (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value += (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value += (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value -= (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value -= (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value -= (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))
            
            else:
                if s.count('1111') > 0:
                    return -1e9
                if s.count('2222') > 0:
                    return 1e9
                ai_value -= (s.count('1110') + s.count('0111') + s.count('1011') + s.count('1101'))*3
                ai_value -= (s.count('1100') + s.count('0110') + s.count('0011') + s.count('1001') + s.count('1010') + s.count('0101'))*2
                ai_value -= (s.count('1000') + s.count('0100') + s.count('0010') + s.count('0001'))

                ai_value += (s.count('2220') + s.count('0222') + s.count('2022') + s.count('2202'))*3
                ai_value += (s.count('2200') + s.count('0220') + s.count('0022') + s.count('2002') + s.count('2020') + s.count('0202'))*2
                ai_value += (s.count('2000') + s.count('0200') + s.count('0020') + s.count('0002'))
        
        return ai_value
    
PLAYER_NUMBER = 2
ai = AIPlayer(PLAYER_NUMBER)

print(board)

print('')

print('')
ai.get_alpha_beta_move(board)
