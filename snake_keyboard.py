# from snake import DIRECTIONS, HEAD
from copy import copy
from snake import APPLE, BODY, MAX_SPEED, MOVEMENT_MAP
from blessed import Terminal
from collections import deque
import random
import copy
from collections import deque

## Some global parameters declaration.
term = Terminal()   # This takes care of all the operations realted to the terminals

SPACE = ' '
SNAKE = '0'
HEAD = '🟥'
FOOD = '🍎'
BORDER = '⬜️'
REWARD = 10
PENALTY = -10
VEL_INC = 0.2   # check whether it becomes applicable or not.
messages = ['Try again !!', 'Game Over !!', 'Better Luck next Time !!', 'Never Give Up']
# we will use random.choice() to pick a random message from above.

# N1 and N2 represents the snake's movement frequency.
# The snake will only move N1 out of N2 turns.
N1 = 1
N2 = 2

# Movement mapping 
LEFT = term.KEY_LEFT
RIGHT = term.KEY_RIGHT
UP = term.KEY_UP
DOWN = term.KEY_DOWN
DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
DIRECTIONS_MAPPING = {LEFT: [0,-1], RIGHT: [0,1],UP: [-1, 0], DOWN: [1,0]}
WASD_MAPPING = {'w': UP, 'a': LEFT,'s': DOWN,'d': RIGHT, 'W': UP,'A': LEFT,'S': DOWN,'D': RIGHT}

height, width = 10, 15
'''
gave the initial coordinates of the snake body
'''
# Defining snake body
snake_body = deque([[6, 5], [6, 4], [6, 3]])     # deque(maxlen=131)
food = [5, 10]

speed = 3
# print(BORDER)
M = 9
# making the world

messages = ['you can do it!', "don't get eaten!", 'run, forest, run!', "where there's a will, there's a way", "you can beat it!", "outsmart the snake!"]
message = None


with term.cbreak(), term.hidden_cursor():

    WORLD = [[SPACE]*width for _ in range(height)]

    print(term.home + term.clear)
    for i in range(height):
        WORLD[i][-1] = BORDER
        WORLD[i][0] = BORDER

    for j in range(width):
        WORLD[0][j] = BORDER
        WORLD[-1][j] = BORDER

    for b_part in snake_body:
        WORLD[b_part[0]][b_part[0]] = SNAKE

    head = snake_body[0]
    WORLD[head[0]][head[1]] = HEAD
    WORLD[food[0]][food[1]] = FOOD
    
    # printing the world

    for row in WORLD:
        print(' '.join(row))
    print('use arrow keys or WASD to move!')
    print("this time, you're the food 😱\n")
    print('I recommend expanding the terminal window')
    print('so the game has enough space to run')

    val = ' '
    moving = False
    turn = 0
    # dead = False

    while True:   
        
        '''Here, we will have infinite loop which will run untill 'q' is pressed from keyboard.
        Use the arrow keys to control the snake.'''

        # see the input from keybord

        val = term.inkey(timeout = 1/speed)
        if val.code in DIRECTIONS or val in WASD_MAPPING.keys():
            moving = True   # as moving start snake will also move
        if not moving:
            continue  # just loop out of..

        # Path planning or The hard core AI

        head = snake_body[0]
        x_diff = food[0] - head[0]
        y_diff = food[1] - head[1]

        ## looking at the difference above we will try to fetch the preferred move.

        if abs(y_diff) >= abs(x_diff):
            if y_diff <= 0:
                preferred_move = UP
            else:
                preferred_move = DOWN
        else:
            if x_diff >= 0:
                preferred_move = RIGHT
            else:
                preferred_move = LEFT
        
        preferred_move = [preferred_move] + list(DIRECTIONS)

        ## we got the preferred move form hard code AI, now implementing it.

        for move in preferred_move:
            move_num = MOVEMENT_MAP[move]  # this will give the number of ++ or --
            head_copy = copy.copy(head)
            head_copy[0] += move_num[0]
            head_copy[1] += move_num[1]
            heading = WORLD[head_copy[0]][head_copy[1]]
            if heading == BORDER:
                continue
            elif heading == BODY:
                if head_copy == snake_body[-1] and turn % M == 0:
                    next_move = head_copy
                    break
                else:
                    continue
            
            else:
                next_move = head_copy
        
        if next_move is None:
            break

        turn += 1
            
        WORLD[food[0]][food[1]] = SPACE
        if turn % N2 < N1:
            snake_body.appendleft(next_move)
            # for every M turns or so, the snake will grow longer and faster.
            WORLD[head[0]][head[1]] = BODY
            if turn % M != 0:
                speed = min(speed*1.05, MAX_SPEED)
                tail = snake_body.pop()
                WORLD[tail[0]][tail[1]] = SPACE
            WORLD[next_move[0]][next_move[1]] = HEAD

        food_copy = copy.copy(food)

        if val.code in DIRECTIONS or val in WASD_MAPPING.keys():
            direction = None
            if val in WASD_MAPPING.keys():
                direction = WASD_MAPPING[val]
            else:
                direction = val.code
            movement = MOVEMENT_MAP[direction]
            food_copy[0] += movement[0]
            food_copy[1] += movement[1]
        
        food_heading = WORLD[food_copy[0]][food_copy[1]]

        if food_heading == HEAD:
            dead = True

        if food_heading == SPACE:
            food = food_copy

        if WORLD[food[0]][food[1]] == BODY or WORLD[food[0]][food[1]] == HEAD:
            dead = True
        if not dead:
            WORLD[food[0]][food[1]] = APPLE
        
        print(term.move_yx(0, 0))
        for row in WORLD:
            print(' '.join(row))
        score = len(snake_body) - 3
        print(f'score: {turn} - size: {len(snake_body)}' + term.clear_eol)

        if dead:
            break
        if turn % 50 == 0:
            message = random.choice(messages)
        if message:
            print(message + term.clear_eos)
        print(term.clear_eos, end='')

if dead:
  print('you were eaten by the snake!' + term.clear_eos)
else:
  print('woah you won!! how did you do it?!' + term.clear_eos)



        # def isCollision():
        #     '''
        #     Collision between walls or between the snake and its body
        #     '''
        #     for i, j in zip(range(height, width)):
        #         pass

    




    
    










