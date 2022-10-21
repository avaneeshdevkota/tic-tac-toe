"""
Tic Tac Toe Player
"""


import math
import copy
import sys
from xml.dom import InvalidAccessErr

X = "X"
O = "O"
EMPTY = None


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

    count = 0
    for row in board:
        for cell in row:
            if (cell != EMPTY):
                count += 1

    if (count%2 == 0):
        return "X"
    return "O"

def actions(board):

    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                possible_actions.add((i,j))

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if (board[action[0]][action[1]] != None):
        raise InvalidAccessErr
    
    resultant_board = copy.deepcopy(board)
    resultant_board[action[0]][action[1]] = player(board)
    return resultant_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        row_set = set(row)
        if len(row_set) == 1 and None not in row_set:
            if ("O" in row_set):
                return "O"
            return "X"

    for i in range(3):
        col_set = set()
        for j in range(3):
            col_set.add(board[j][i])
        if len(col_set) == 1 and None not in col_set:
            if ("O" in col_set):
                return "O"
            return "X"
    
    diag_set_down = set()
    diag_set_up = set()
    for i in range(3):
        diag_set_down.add(board[i][i])
        diag_set_up.add(board[2-i][i])
    if (len(diag_set_down) == 1 and None not in diag_set_down):
        if ("O" in diag_set_down):
            return "O"
        return "X"

    if (len(diag_set_up) == 1 and None not in diag_set_up):
        if ("O" in diag_set_up):
            return "O"
        return "X"

def terminal(board):

    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    won = winner(board)

    if (won == "X"):
        return 1
    elif (won == "O"):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board)):
        return None

    current_player = player(board)

    if (current_player == "X"):

        possible_moves = actions(board)
        value = -sys.maxsize
        best_move = None

        for move in possible_moves:
            resultant_state = result(board, move)
            if (minimizer(resultant_state) > value):
                best_move = move
                value = minimizer(resultant_state)

    else:

        possible_moves = actions(board)
        value = sys.maxsize
        best_move = None

        for move in possible_moves:
            resultant_state = result(board, move)
            if (maximizer(resultant_state) < value):
                best_move = move
                value = maximizer(resultant_state)

    return best_move

def minimizer(board):

    if terminal(board):
        return utility(board)

    min_val = sys.maxsize
    possible_moves = actions(board)

    for move in possible_moves:
        resultant_state = result(board,move)
        min_val = min(min_val, maximizer(resultant_state))
    return min_val

def maximizer(board):  

    if terminal(board):
        return utility(board)

    max_val = -sys.maxsize
    possible_moves = actions(board)

    for move in possible_moves:
        resultant_state = result(board,move)
        max_val = max(max_val, minimizer(resultant_state))
    return max_val