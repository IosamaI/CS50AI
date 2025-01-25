"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    countX = 0
    countO = 0
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == X:
                countX += 1
            elif board[row][column] == O:
                countO += 1

    return X if countX == countO else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_movie = set()

    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == EMPTY:
                possible_movie.add((row, column))

    return possible_movie


def result(board, action):
    # Destructure action to row and column
    row, col = action

    # Check if the action is within the board bounds
    if row < 0 or row > 2 or col < 0 or col > 2:
        raise ValueError("Action is out of bounds")

    # Check if the target cell is empty
    if board[row][col] != EMPTY:
        raise ValueError("Cell is already occupied")

    # Make a copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]

    # Apply the action (set the cell to the current player's symbol)
    current_player = player(board)
    new_board[row][col] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns for a winner
    for col in range(3):
        if (
            board[0][col] == board[1][col] == board[2][col]
            and board[0][col] is not EMPTY
        ):
            return board[0][col]

    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) is not None:
        return True

    # Check if the board is full
    for row in board:
        if EMPTY in row:
            return False

    # If no winner and no empty cells, the game is over
    return True


def utility(board):
    """
    Returns the utility of the board:
    1 if X has won, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal move for the current player on the given board.
    If the game is over (terminal board), it returns None.
    """
    if terminal(board):  # If the game is over, no moves can be made
        return None

    # Get all possible actions (moves) for the current player
    possible_actions = actions(board)

    # If it's X's turn (maximizing player)
    if player(board) == X:
        best_score = -float("inf")  # Start with a very low score
        best_move = None
        for action in possible_actions:
            new_board = result(board, action)
            score = minimax_score(new_board)  # Get the score for this move
            if score > best_score:  # Maximize the score
                best_score = score
                best_move = action
        return best_move

    # If it's O's turn (minimizing player)
    else:
        best_score = float("inf")  # Start with a very high score
        best_move = None
        for action in possible_actions:
            new_board = result(board, action)
            score = minimax_score(new_board)  # Get the score for this move
            if score < best_score:  # Minimize the score
                best_score = score
                best_move = action
        return best_move


def minimax_score(board):
    """
    Recursively calculates the score of the board for Minimax.
    The score is the utility of the board.
    """
    # If the game is over, return the utility of the board
    if terminal(board):
        return utility(board)

    # If it's X's turn (maximize), we want the max score
    if player(board) == X:
        best_score = -float("inf")
        for action in actions(board):
            new_board = result(board, action)
            best_score = max(best_score, minimax_score(new_board))
        return best_score

    # If it's O's turn (minimize), we want the min score
    else:
        best_score = float("inf")
        for action in actions(board):
            new_board = result(board, action)
            best_score = min(best_score, minimax_score(new_board))
        return best_score
