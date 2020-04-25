"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def countXO(board):
    """
    Counts number of X's and O's on the board.
    """
    xCount = oCount = 0
    for row in board:
        for cell in row:
            if      cell == X:   xCount += 1 
            elif    cell == O:   oCount += 1
    return xCount, oCount


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """    
    xCount, oCount = countXO(board)
    if      xCount <= oCount: return X 
    elif    xCount >  oCount: return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allowedActions = set((i,j) for i in range(3) for j in range(3) if board[i][j] is EMPTY)            #;print(f'{allowedActions=}')                                                
    return allowedActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action

    if board[i][j] is not EMPTY: raise Exception(f'Invalid action {action} on board: {board}')

    new_board = deepcopy(board)
    new_board[i][j] = player(board)
    return new_board
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in [X,O]:
        for rowIdx, row in enumerate(board):
            if all([row[0]==player, row[1]==player, row[2]==player]): 
                # print(f'{player} wins on row: {rowIdx}')
                return player
    
            for colIdx, cell in enumerate(row):
                try:
                    if all([board[rowIdx][colIdx]==player, board[rowIdx+1][colIdx]==player, board[rowIdx+2][colIdx]==player]): 
                        # print(f'{player} wins on column: {colIdx}')
                        return player

                    if all([board[rowIdx][colIdx]==player, board[rowIdx+1][colIdx+1]==player, board[rowIdx+2][colIdx+2]==player]): 
                        # print(f'{player} wins on the main diagonal')
                        return player

                    if all([board[rowIdx][len(row)-1]==player, board[rowIdx+1][len(row)-2]==player, board[rowIdx+2][len(row)-3]==player]): 
                        # print(f'{player} wins on the antidiagonal')
                        return player
                except IndexError:
                    pass

    # print('No winner')
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    xCount, oCount = countXO(board)
    return winner(board) or (xCount+oCount == 9)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winningPlayer = winner(board)
    if      winningPlayer == X:     return 1
    elif    winningPlayer == O:     return -1
    elif    winningPlayer is None:  return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board, alpha, beta):
        if terminal(board): return utility(board)
        # print(f'\nmax_value() : {board=}')
        v = float('-inf')
        for action in actions(board):
            # print(f'max_value() : {action=}')
            board_new = result(board, action)       #;print(f'max_value() : {board_new=}')
            min_val = min_value(board_new, alpha, beta)          #;print(f'max_value() : {min_val=}')
            v = max(v, min_val)
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v

    def min_value(board, alpha, beta):
        if terminal(board): return utility(board)
        # print(f'\nmin_value() : {board=}')
        v = float('inf')
        for action in actions(board):
            # print(f'min_value() : {action=}')
            board_new = result(board, action)       #;print(f'min_value() : {board_new=}')
            max_val = max_value(board_new, alpha, beta)          #;print(f'min_value() : {max_val=}')
            v = min(v, max_val)
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v


    if terminal(board): return None

    currentPlayer = player(board) 
    optimal_action = None
    inf_neg = float('-inf')
    inf_pos = float('inf')
    
    if currentPlayer == X: 
        v = inf_neg
        for action in actions(board):
            min_val = min_value(result(board, action), inf_neg, inf_pos)
            if min_val > v:
                v = min_val
                optimal_action = action
    elif currentPlayer == O:
        v = inf_pos
        for action in actions(board):
            max_val = max_value(result(board, action), inf_neg, inf_pos)
            if max_val < v:
                v = max_val
                optimal_action = action
    
    return optimal_action
