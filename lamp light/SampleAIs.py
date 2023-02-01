import random

# Moves are of the form [row, col] where those are the coordinates where you want to place your light.
# Your move must be a pair of integers, not floats or anything else.
# The board is a 2D array of squares which are represented as length 5 lists: [you, p1, p2, p3, point value]
# Whoever, ties go to nobody, has the most in each square wins that square


def RandomRandy(board, walls):
    return [random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)]


def CenterCarly(board, walls):
    return [int(len(board)//2), int(len(board)//2)]


def NihilNelly(board, walls):
    return [-1, -1]


def whose_square(board, row, col):  # Determines who controls the square, ties go to nobody
    square = board[row][col]
    winner = None
    maximum = -1
    for player in range(4):
        if square[player] > maximum:
            winner = player
            maximum = square[player]
        elif square[player] == maximum:
            winner = None
    return winner


def own_score(board):  # Calculates the current score of the player with index player_index.
    score = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if whose_square(board, i, j) == 0:
                score += board[i][j][4]
    return score


def ProtectivePeter(board, walls):  # Prefers to play in its own squares
    found = False
    while not found:
        square = [random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)]
        if whose_square(board, square[0], square[1]) == 0:
            found = True
        elif random.randint(0, 19) == 0:  # A precautionary measure to stop infinite loops.
            found = True
    return square


def AggressiveAndy(board, walls):
    found = False
    while not found:
        square = [random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)]
        if whose_square(board, square[0], square[1]) != 0:
            found = True
        elif random.randint(0, 19) == 0:  # A precautionary measure to stop infinite loops.
            found = True
    return square
