# A prototype Jigga Jigga program
# Created by Alex Z
# Started 2021/06/16

# Import libraries

import pygame, random, copy, os, time
# Initializing the pygame screen variables.
pygame.init()
# Putting the window in the center of the screen
screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h
x = round((screen_w - 820) / 2)
y = round((screen_h - 500) / 2 * 0.8)  # 80 % of the actual height
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
screen = pygame.display.set_mode((820, 500))  # Creating the display screen.


# Initializing board variables

scores = [0, 0, 0, 0]  # the scores of the players
round_number = 0
size = 20  # Size of the board
board = [[[0, 0, 0, 0, 1] for i in range(size)] for j in range(size)]  # Entries of the form: [l1, l2, l3, l4, p]
walls = [[[4,4], [4,7]], [[4,4], [7,4]], [[size-4,4], [size-4,7]], [[4,size-4], [4,size-7]], [[size-4,size-4], [size-4,size-7]],
         [[size-4,4], [size-7,4]], [[4,size-4], [7,size-4]], [[size-4,size-4], [size-7,size-4]]]
# representing the light levels of players 1, 2, 3, and 4, and the point value of the square respectively.

PlayerAIs = []  # A list of all the imported functions.
PlayerColors = []  # A list of all the colors of the players
PlayerNames = []  # A list of the names of the players

# Import your AI here:

from SampleAIs import NihilNelly
from SampleAIs import RandomRandy
from SampleAIs import CenterCarly
from SampleAIs import ProtectivePeter
from SampleAIs import AggressiveAndy
from SampleAIs import SillySnake
from SampleAIs import RightSnake
from SampleAIs import SetSnake

PlayerAIs.append(NihilNelly)
PlayerColors.append([0, 0, 0])
PlayerNames.append("Nihil Nelly")

PlayerAIs.append(RandomRandy)
PlayerColors.append([1, 0, 0])
PlayerNames.append("Random Randy 1")

PlayerAIs.append(RandomRandy)
PlayerColors.append([0, 0, 1])
PlayerNames.append("Random Randy 2")

PlayerAIs.append(RandomRandy)
PlayerColors.append([1, 1, 0])
PlayerNames.append("Random Randy 3")

PlayerAIs.append(CenterCarly)
PlayerColors.append([0, 1, 0])
PlayerNames.append("Center Carly")

PlayerAIs.append(ProtectivePeter)
PlayerColors.append([.5, 0, .5])
PlayerNames.append("Protective Peter")

PlayerAIs.append(AggressiveAndy)
PlayerColors.append([0, 1, 1])
PlayerNames.append("Aggressive Andy")

PlayerAIs.append(SillySnake)
PlayerColors.append([1, .5, 0])
PlayerNames.append("Silly Snake")

PlayerAIs.append(RightSnake)
PlayerColors.append([.2, .6, .4])
PlayerNames.append("Right Snake")

PlayerAIs.append(SetSnake)
PlayerColors.append([.4, .2, .6])
PlayerNames.append("Set Snake")


def importAI(AIFileName, AIFunc, AIColor, AIName): # A function for importing your AI. Do not include .py in the file name. Be sure that AIFileName and AIFunc are strings
    exec("from " + AIFileName + " import " + AIFunc)
    exec("PlayerAIs.append(" + AIFunc + ")")
    PlayerColors.append(AIColor)
    PlayerNames.append(AIName)

importAI("SampleAIs", "DarkestDandy", [.3,.3,.5], "Darkest Dandy")

# from yourFileName import yourAI
# PlayerAIs.append(yourAI)
# PLayerColors.append(yourAIColor) # in [r,g,b] format (use values between 1 and 0)
# PlayerNames.append(yourAIName)  # as a string

PlayerNumbers = [int(input("Enter the number of player " + str(i + 1) + ": ")) for i in range(4)]  # Inputting the AIs used.

Players = [PlayerAIs[PlayerNumbers[i]] for i in range(4)]  # Creating the player list
colors = [PlayerColors[PlayerNumbers[i]] for i in range(4)]  # The colors of the players
scores = [0 for i in range(4)]


def calculate_score(player_index):  # Calculates the current score of the player with index player_index.
    score = 0  # Temporary score variable
    for i in range(size):  # Iterating over the board
        for j in range(size):
            if whose_square(i, j) == player_index:
                score += board[i][j][4]
    return score

# The section of code starting here:
def onSegment(p, q, r):
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False
# and ending here was retrieved from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/


def check_sees(pos, light, walls):
    for wall in walls:
        if doIntersect([pos[0] + .5, pos[1] + .5], [light[0] + .5, light[1] + .5], wall[0], wall[1]):
            return False
    return True

def add_lights(list, banned_indexes=[], walls=walls):  # Adds a light for a player at the position given.
    for i in range(size):
        for j in range(size):
            index = 0
            for row, col in list:
                if index not in banned_indexes and check_sees([i,j], [row,col], walls):
                    distance_squared = (abs(row - i) + 1/2) ** 2 + (abs(col - j) + 1/2) ** 2
                    board[i][j][index] += 1 / distance_squared
                index += 1


def process_board(player_index):  # Converts the board to the state that your AI will receive it.
    new_board = []  # Initializing the new board.
    for row in board:
        new_row = []
        for square in row:
            new_square = []
            for i in range(4):  # Reindexing the board to make your AI index 0.
                new_square.append(square[(i + player_index) % 4])
            new_square.append(square[4])
            new_row.append(new_square)
        new_board.append(new_row)
    return new_board


def whose_square(row, col):  # Determines who controls the square, ties go to nobody
    square = board[row][col]
    winner = None
    maximum = 0
    for player in range(4):
        if square[player] > maximum:
            winner = player
            maximum = square[player]
        elif square[player] == maximum:
            winner = None
    return winner


def get_square_color(square):
    color = [0, 0, 0]
    for i in range(4):
        for j in range(3):
            color[j] += max(0,square[i] * PlayerColors[PlayerNumbers[i]][j])
    return color


def display(screen):
    cell_width = 20
    screen.fill([0, 0, 0])  # Clears the screen with black.
    pygame.draw.rect(screen, [63, 63, 63], [40, 40, 420, 420])
    pygame.draw.rect(screen, [200, 200, 200], [46, 46, 408, 408])
    # Drawing the board
    for i in range(size):
        for j in range(size):
            square = board[i][j][:4]
            # Determining the color of each square.
            color = [min(255, int(255 * (1 - 1 / (2 ** (get_square_color(square)[0] / 1.5))))),
                     min(255, int(255 * (1 - 1 / (2 ** (get_square_color(square)[1] / 1.5))))),
                     min(255, int(255 * (1 - 1 / (2 ** (get_square_color(square)[2] / 1.5)))))]

            pygame.draw.rect(screen, color, [50 + (cell_width * i), 50 + (cell_width * j), cell_width,
                                             cell_width])  # Draws the square.

    for wall in walls:
        pygame.draw.line(screen, (100, 100, 100), [wall[0][0]*cell_width+50-1, wall[0][1]*cell_width+50-1], [wall[1][0]*cell_width+50-1, wall[1][1]*cell_width+50-1], width=8)

    for i in range(size):
        for j in range(size):
            # Determining whether there is a border.
            player = whose_square(i, j)
            neighbors = [[-1, 0], [0, -1], [1, 0], [0, 1]]
            for neighbor in neighbors:
                if 0 <= i + neighbor[0] < size and 0 <= j + neighbor[1] < size:
                    if player != whose_square(i + neighbor[0], j + neighbor[1]):  # Drawing the boarders
                        if player is None:
                            color = [15, 15, 15]
                        else:
                            color = [colors[player][0]*255, colors[player][1] * 255, colors[player][2] * 255]
                        pygame.draw.rect(
                            screen,
                            color,
                            [50 + (cell_width//2-1) + cell_width * i + (cell_width//2-1) * neighbor[0] - (cell_width//2-1) * abs(neighbor[1]),
                             50 + (cell_width//2-1) + cell_width * j + (cell_width//2-1) * neighbor[1] - (cell_width//2-1) * abs(neighbor[0]),
                             ((cell_width -2) * abs(neighbor[1])) + 2,
                             ((cell_width -2) * abs(neighbor[0])) + 2])
    for player_index in range(4):  # Displays the points of each player.
        name = PlayerNames[PlayerNumbers[player_index]]
        color = [colors[player_index][0] * 255, colors[player_index][1] * 255, colors[player_index][2] * 255]
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        scores[player_index] += calculate_score(player_index)*.01 # Gives each player cumulative points
        text = font.render(name + " : " + str(scores[player_index] + calculate_score(player_index))[0:6], False, color)
        screen.blit(text, [100 + 20 * size, 80 + 90 * player_index])
        pygame.draw.rect(screen, color, [105 + 20 * size, 110 + 90 * player_index, int(scores[player_index]//3), 8])
    font40 = pygame.font.Font(pygame.font.get_default_font(), 40)
    text = font40.render("Lamp Light", False, (255,255,255))
    screen.blit(text, [110 + 20 * size, 15])


def decay():  # Runs the decay step.
    for i in range(size):
        for j in range(size):
            for player in range(4):
                board[i][j][player] *= .96
                if board[i][j][player] > 0:
                    board[i][j][player] -= .01
                    if board[i][j][player] < 0:
                        board[i][j][player] = 0


def run_round(screen):  # Runs one turn of the game.
    global round_number

    moves = []  # Each move is of the form [row, col].
    for i in range(4):
        start = time.time_ns() # Your function must return a response within .1 seconds
        try:
            moves.append(Players[i](process_board(i), copy.copy(walls)))# Getting the moves of each player.
        except:
            try:
                moves.append(Players[i](process_board(i))) # In case you forgot the walls argument
            except:
                print("Your Function is throwing an error please check it. Your strategy will forfet its turn.")
                print(process_board(i))
                print(walls)
                # This is for your debugging purposes
                moves.append([-1,-1])
        stop = time.time_ns()
        if stop - start > 100000000:
            print("Your function is taking too long: " + str(PlayerNames[PlayerNumbers[i]]))


    banned_indexes = []  # Checking whether all the moves are legal
    for i in range(4):
        try:
            if moves[i][0] < 0 or moves[i][0] >= size or type(moves[i][0]) != type(1) or\
                moves[i][1] < 0 or moves[i][1] >= size or type(moves[i][1]) != type(1):
                banned_indexes.append(i)
        except AttributeError or IndexError:
            banned_indexes.append(i)

    add_lights(moves, banned_indexes=banned_indexes)  # Resolving each move.

    decay()  # Makes the entire screen dimmer

    display(screen)  # Draws the screen

    if round_number >= 300:
        return

    pygame.display.flip()  # Updates the screen.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    pygame.time.wait(100)
    round_number += 1
    run_round(screen)

display(screen)
pygame.display.flip()
time.sleep((1))
# Here's some added bgm for you
song_names = ["Lensko - Titsepoken 2015 [NCS Release].mp3",
              "Tobu & Itro - Sunburst [NCS Release].mp3",
              "Tobu - Candyland [NCS Release].mp3",
              "Tobu - Good Times [NCS Release].mp3",
              "Tobu - Roots [NCS Release].mp3",
              "Verm - Explode [NCS Release].mp3",
              "Warptech - Last Summer [NCS Release].mp3"]
channel = pygame.mixer.find_channel()
channel.set_volume(.8)
channel.play(pygame.mixer.Sound("Game Music/" + random.choice(song_names)))
run_round(screen)
for i in range(4):
    print(PlayerNames[PlayerNumbers[i]] + ": " + str(scores[i] + calculate_score(i)))
for i in range(80,10,-1):
    channel.set_volume(i/100)
    time.sleep(.01)
flag = True
while flag:
    if not channel.get_busy():
        channel.play(pygame.mixer.Sound("Game Music/" + random.choice(song_names)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.K_RETURN in pygame.key.get_pressed()):
            flag = False
            break
channel.stop()
pygame.quit()
