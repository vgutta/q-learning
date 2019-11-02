import sys # used for bash args
from random import randint # used tp ick random values

goal1 = int(sys.argv[1])
goal2 = int(sys.argv[2])
forbidden = int(sys.argv[3])
wall = int(sys.argv[4])
letter = sys.argv[5]
index = None
if letter == 'q':
    index = int(sys.argv[6])

living_reward = -0.1
discount_rate = 0.2
learning_rate = 0.1

board_size = 4
start = 2
current = start

class Tile: # class to create instance for each tile
    def __init__(self, north, east, south, west, id, tiletype):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.id = id
        self.tiletype = tiletype # to store input states and start state

# returns direction based on each directions q value give a tile
def bestdirection(tile): 
    action = "north"
    largest = tile.north
    if largest < tile.east:
        action = "east"
        largest = tile.east
    if largest < tile.south:
        action = "south"
        largest = tile.south
    if largest < tile.west:
        action = "west"
        largest = tile.west
    return action

# function to set locations of tiles given through input
def setInputTiles(board): 
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j].id == goal1:
                board[i][j].tiletype = 'goal1'
            if board[i][j].id == goal2:
                board[i][j].tiletype = 'goal2'
            if board[i][j].id == forbidden:
                board[i][j].tiletype = 'forbidden'
            if board[i][j].id == wall:
                board[i][j].tiletype = 'wall'

# returns if give location is a goal or forbidden state
def exitstate(location):
    if location == goal1 or location == goal2 or location == forbidden:
        return False
    else:
        return True

# searches and returns instance for a tile given a location
def locateTile(location):
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j].id == location:
                return board[i][j]

# return new direction or best direction based on q values
def nextAction(currentTile):
    actrandomly = randint(1, 10) # act randomly 10% of the time
    direction = randint(1, 4)
    if actrandomly == 1: # 10% chance of 1(act randomly)
        if direction == 1:
            return 'north'
        elif direction == 2:
            return 'east'
        elif direction == 3:
            return 'south'
        elif direction == 4:
            return 'west'
    else:
        return bestdirection(currentTile)

# returns next state given current state and direction
def nextState(current, action):
    nextLocation = 0
    if action == 'north':
        if current == 13 or current == 14 or current == 15 or current == 16:
            nextLocation = current # out of range
        else:
            nextLocation = current + 4
    elif action == 'east':
        if current == 4 or current == 8 or current == 12 or current == 16:
            nextLocation = current # out of range
        else:
            nextLocation = current + 1
    elif action == 'south':
        if current == 1 or current == 2 or current == 3 or current == 4:
            nextLocation = current # out of range
        else:
            nextLocation = current - 4
    elif action == 'west':
        if current == 1 or current == 5 or current == 9 or current == 13:
            nextLocation = current # out of range
        else:
            nextLocation = current - 1
    if nextLocation == wall: # if wall remain in current location
        nextLocation = current
    return nextLocation

# returns reward based on tile type
def reward(nextTile):
    if nextTile.tiletype == 'goal1' or nextTile.tiletype == 'goal2':
        return 100
    elif nextTile.tiletype == 'forbidden':
        return -100
    else:
        return -0.1

# returns max q if tile is not an exit state
def maxq(nextTile):
    if nextTile.tiletype == 'goal1' or nextTile.tiletype == 'goal2' or nextTile.tiletype == 'forbidden':
        return 0
    else:
        return max(nextTile.north, nextTile.east, nextTile.south, nextTile.west)

# compute q values based on current tile, next tile, and action direction
def computeq(action, currentTile, nextTile):
    if action == 'north':
        currentTile.north = (1 - learning_rate) * currentTile.north + learning_rate * (reward(nextTile) + discount_rate * maxq(nextTile))
    elif action == 'east':
        currentTile.east = (1 - learning_rate) * currentTile.east + learning_rate * (reward(nextTile) + discount_rate * maxq(nextTile))
    elif action == 'south':
        currentTile.south = (1 - learning_rate) * currentTile.south + learning_rate * (reward(nextTile) + discount_rate * maxq(nextTile))
    elif action == 'west':
        currentTile.west = (1 - learning_rate) * currentTile.west + learning_rate * (reward(nextTile) + discount_rate * maxq(nextTile))
    
# main function 
def qlearning(board):
    current = start
    for _ in range(10000):
        while exitstate(current):
            currentTile = locateTile(current)
            action = nextAction(currentTile)
            nextLocation = nextState(current, action)
            nextTile = locateTile(nextLocation)
            computeq(action, currentTile, nextTile)
            current = nextState(current, action)
        current = start # returns to start after exit state

def printqvalues(board, index):
    for j in range(board_size):
        for i in range(board_size):
            if board[i][j].id == index:
                print("↑", board[i][j].north)
                print("→", board[i][j].east)
                print("←", board[i][j].west)
                print("↓", board[i][j].south)


#Function to print the policy
def printPolicy(board):
    low = 0
    high = 0
    looper = 1
    while looper < 5:
        for j in range(board_size):
            for i in range(board_size):
                if looper == 1:
                    low = 1
                    high = 4
                elif looper == 2:
                    low = 5
                    high = 8
                elif looper == 3:
                    low = 9
                    high = 12
                elif looper == 4:
                    low = 13
                    high = 16
                if board[i][j].id >= low and board[i][j].id <= high and board[i][j].tiletype != "wall" and board[i][j].tiletype != "goal1" and board[i][j].tiletype != "goal2" and board[i][j].tiletype != "forbidden":
                    if bestdirection(board[i][j]) == "north":
                        print("↑", board[i][j].id)
                    elif bestdirection(board[i][j]) == "east":
                        print("→", board[i][j].id)
                    elif bestdirection(board[i][j]) == "south":
                        print("↓", board[i][j].id)
                    elif bestdirection(board[i][j]) == "west":
                        print("←", board[i][j].id)
        looper += 1

# initialize 16 tiles and specify start state
tile1 = Tile(0, 0, 0, 0, 1, None)
tile2 = Tile(0, 0, 0, 0, 2, 'Start')
tile3 = Tile(0, 0, 0, 0, 3, None)
tile4 = Tile(0, 0, 0, 0, 4, None)
tile5 = Tile(0, 0, 0, 0, 5, None)
tile6 = Tile(0, 0, 0, 0, 6, None)
tile7 = Tile(0, 0, 0, 0, 7, None)
tile8 = Tile(0, 0, 0, 0, 8, None)
tile9 = Tile(0, 0, 0, 0, 9, None)
tile10 = Tile(0, 0, 0, 0, 10, None)
tile11 = Tile(0, 0, 0, 0, 11, None)
tile12 = Tile(0, 0, 0, 0, 12, None)
tile13 = Tile(0, 0, 0, 0, 13, None)
tile14 = Tile(0, 0, 0, 0, 14, None)
tile15 = Tile(0, 0, 0, 0, 15, None)
tile16 = Tile(0, 0, 0, 0, 16, None)

# store the 16 tiles in corresponding 2D array location
board = [[tile13, tile14, tile15, tile16],
         [tile9, tile10, tile11, tile12],
         [tile5, tile6, tile7, tile8],
         [tile1, tile2, tile3, tile4]]

setInputTiles(board) # set input tiles and their types in the corresponding location

qlearning(board) # main function

if letter == 'p':
    printPolicy(board)
if letter == 'q':
    printqvalues(board, index)