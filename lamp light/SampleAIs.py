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


def AggressiveAndy(board, walls): # Trys to play on opponent's squares
    found = False
    while not found:
        square = [random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)]
        if whose_square(board, square[0], square[1]) != 0:
            found = True
        elif random.randint(0, 19) == 0:  # A precautionary measure to stop infinite loops.
            found = True
    return square

SillySnakeSpot = [random.randint(0,19), random.randint(0,19)]
sillyheading = random.randint(0,3)

def SillySnake(board, walls): # Places lights in a snake's path
    global sillyheading, SillySnakeSpot
    if sillyheading == 0:
        SillySnakeSpot = [(SillySnakeSpot[0]+1)%20,SillySnakeSpot[1]]
    if sillyheading == 1:
        SillySnakeSpot = [SillySnakeSpot[0],(SillySnakeSpot[1]+1)%20]
    if sillyheading == 2:
        SillySnakeSpot = [(SillySnakeSpot[0]-1)%20,SillySnakeSpot[1]]
    if sillyheading == 3:
        SillySnakeSpot = [SillySnakeSpot[0],(SillySnakeSpot[1]-1)%20]
    sillyheading = random.choice([sillyheading, sillyheading, sillyheading, (sillyheading-1)%4, (sillyheading+1)%4])
    return SillySnakeSpot

RightSnakeSpot = [random.randint(0,4), random.randint(0,4)]
rightheading = 0

def RightSnake(board, walls):
    global rightheading, RightSnakeSpot
    if rightheading == 0:
        RightSnakeSpot = [(RightSnakeSpot[0] + 1) % 20, RightSnakeSpot[1]]
    if rightheading == 1:
        RightSnakeSpot = [RightSnakeSpot[0], (RightSnakeSpot[1] + 1) % 20]
    if rightheading == 2:
        RightSnakeSpot = [(RightSnakeSpot[0] - 1) % 20, RightSnakeSpot[1]]
    if rightheading == 3:
        RightSnakeSpot = [RightSnakeSpot[0], (RightSnakeSpot[1] - 1) % 20]
    if random.randint(0,7) == 0:
        rightheading = (rightheading+1)%4
    return RightSnakeSpot

SetSnakeSpot = [2,2]
setheading = 0
setcount = 0

def SetSnake(board, walls):
    global setheading, SetSnakeSpot, setcount
    setcount += 1
    if setheading == 0:
        SetSnakeSpot = [(SetSnakeSpot[0] + 1) % 20, SetSnakeSpot[1]]
    if setheading == 1:
        SetSnakeSpot = [SetSnakeSpot[0], (SetSnakeSpot[1] + 1) % 20]
    if setheading == 2:
        SetSnakeSpot = [(SetSnakeSpot[0] - 1) % 20, SetSnakeSpot[1]]
    if setheading == 3:
        RightSnakeSpot = [SetSnakeSpot[0], (SetSnakeSpot[1] - 1) % 20]
    if setcount%20 == 16:
        setheading = 1
    if setcount%40 == 0:
        setheading = 0
    if setcount%40 == 20:
        setheading = 2
    return SetSnakeSpot

def DarkestDandy(board, walls):
    minlight = 20
    pos = [random.randint(0,len(board)-1),random.randint(0,len(board)-1)]
    for i in range(len(board)):
        for j in range(len(board)):
            mn = max(board[i][j][0:4])
            if mn < minlight and board[i][j][0]:
                minlight = mn
                pos = [i,j]
    return pos