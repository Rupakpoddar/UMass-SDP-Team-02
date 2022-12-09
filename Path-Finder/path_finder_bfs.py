import pygame, sys
from pygame.locals import *
import numpy as np
import time
# Initialize pygame
pygame.init()

gradient = 2
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [700 * gradient, 300 * gradient]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Define some colors
PATH_COLOR = (15, 250, 223)
TRAVERSAL_COLOR = (0, 0, 204)
BACKGROUND = (74, 71, 71)
GRID_COLOR = (0, 0, 0)
WALL_COLOR = (255, 0, 0)
# This sets the WIDTH and HEIGHT of each grid location
GRID_WIDTH = 10 * gradient
GRID_HEIGHT = 10 * gradient
GRID_MARGIN = 2 * gradient
GRID_ROWS = WINDOW_SIZE[1] // (GRID_HEIGHT + GRID_MARGIN)
GRID_COLUMNS = WINDOW_SIZE[0] // (GRID_WIDTH + GRID_MARGIN)
#Start - End
#coordinates on the screen
START_xy = ()
END_xy = ()
#coordinates on the grid
START_Co = ()
END_Co = ()
#start image
s_image = pygame.image.load("./start.png").convert_alpha()
start_image = pygame.transform.scale(s_image, (10 * gradient, 10 * gradient))
#end image
e_image = pygame.image.load("./end.png").convert_alpha()
end_image = pygame.transform.scale(e_image, (10 * gradient, 10 * gradient))
#FLAG PATH
FLAG = False

# _____________________________________MAKE MATRIX_______________________________________________________________
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
parent = []
for row in range(GRID_ROWS + 50):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    parent.append([])
    for column in range(GRID_COLUMNS + 50):
        grid[row].append(1)  # Append a cell
        parent[row].append((-1, -1))
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
# grid[1][5] = 1

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


## ________________________________________________________FUNCTIONS__________________________________________________
def find_path(start, goal):
    #Start Coordinates: StartCo()
    #End Coordinates: EndCo()
    #grid[][]:
    #       -1: start
    #       -2: end
    #       0: wall
    #       1: unvisited adjacent
    #       2: visited adjacent
    #       3: path
    
    print('searching from', start, 'to', goal)
    queue = []
    path = False
    queue.append(start)
    while len(queue) != 0:
        
        node = queue.pop(0)
        #time.sleep(0.5)

        if node == goal:
            path = True
            break
        #__________________________EXPLORE_NODES
        x, y = node
        #Up, Down
        ver = [-1, +1, 0, 0]
        #Left, Right
        hor = [0, 0, +1, -1]
       
        for i in range(4): 
            check_h = hor[i] + x
            check_v = ver[i] + y

            #__________________________manage out of bounds
            if check_v < 0 or check_h < 0:
                continue
            if check_v >= len(grid) or check_h >= len(grid[0]):
                continue
            # if WALL: skip
            if grid[check_h][check_v] == 0:
                continue
            #if visited: skip
            if grid[check_h][check_v] == 2:
                continue
            queue.append((check_h, check_v))
            if (check_h, check_v) != start and (check_h, check_v) != goal:
                grid[check_h][check_v] = 2
            parent[check_h][check_v] = node
            
            pygame.draw.rect(
                screen, TRAVERSAL_COLOR,
                [(GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN,
                 (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN, GRID_WIDTH,
                 GRID_HEIGHT])
            #time.sleep(5)
            pygame.display.update()
            #time.sleep(0.1)
            print(row,column)
           
        ####################################################################
    if path:
        node = goal
        while not (node == start):
            if (check_h, check_v) != start and (check_h, check_v) != goal:
                grid[node[0]][node[1]] = 3
            node = parent[node[0]][node[1]]
    else:
        print(node)
        print(row, column)
        pygame.draw.rect(
                    screen, GRID_COLOR,
                    [(GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN,
                     (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN,
                     GRID_WIDTH, GRID_HEIGHT])
        #time.sleep(5)
        return_path(node, start)
    #print('hey')
    ''' 
    if not path:
        #print('rerun')
        goal = START_Co
        
        find_path(node, goal)
    '''
def return_path(start, goal):
    #Start Coordinates: StartCo()
    #End Coordinates: EndCo()
    #grid[][]:
    #       -1: start
    #       -2: end
    #       0: wall
    #       1: unvisited adjacent
    #       2: visited adjacent
    #       3: path
    
    print('searching from', start, 'to', goal)
    queue = []
    path = False
    queue.append(start)

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 2:
                grid[x][y] = 1
                pygame.draw.rect(
                screen, BACKGROUND,
                [(GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN,
                 (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN, GRID_WIDTH,
                 GRID_HEIGHT])
            
                pygame.display.update()
    
    #time.sleep(5)
    while len(queue) != 0:
        
        node = queue.pop(0)
        #time.sleep(0.5)

        if node == goal:
            path = True
            break
        #__________________________EXPLORE_NODES
        x, y = node
        #Up, Down
        ver = [-1, +1, 0, 0]
        #Left, Right
        hor = [0, 0, +1, -1]
        for i in range(4): 
            check_h = hor[i] + x
            check_v = ver[i] + y

            #__________________________manage out of bounds
            if check_v < 0 or check_h < 0:
                continue
            if check_v >= len(grid) or check_h >= len(grid[0]):
                continue
            # if WALL: skip
            if grid[check_h][check_v] == 0:
                continue
            #if visited: skip
            if grid[check_h][check_v] == 2:
                continue
            queue.append((check_h, check_v))
            if (check_h, check_v) != start and (check_h, check_v) != goal:
                grid[check_h][check_v] = 2
            parent[check_h][check_v] = node
            
            #time.sleep(0.1)
            pygame.draw.rect(
                screen, TRAVERSAL_COLOR,
                [(GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN,
                 (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN, GRID_WIDTH,
                 GRID_HEIGHT])
            
            pygame.display.update()
        ####################################################################
    if path:
        node = goal
        while not (node == start):
            if (check_h, check_v) != start and (check_h, check_v) != goal:
                grid[node[0]][node[1]] = 3
            node = parent[node[0]][node[1]]

def makeWall():
    WALL = True
    while WALL:
        for eventCtrl in pygame.event.get():

            if eventCtrl.type == pygame.KEYDOWN:
                if eventCtrl.key == pygame.K_ESCAPE:
                    done = True
                elif eventCtrl.key != pygame.K_a:
                    WALL = False
                    break
                    '''
                    modsCtrl = pygame.key.get_mods()
                    if modsCtrl & pygame.KMOD_ALT:
                        WALL = False
                        break
                    '''
            elif eventCtrl.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (GRID_WIDTH + GRID_MARGIN)
                row = pos[1] // (GRID_HEIGHT + GRID_MARGIN)
                # Set that location to one
                grid[row][column] = 0
                pygame.draw.rect(
                    screen, WALL_COLOR,
                    [(GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN,
                     (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN,
                     GRID_WIDTH, GRID_HEIGHT])
                pygame.display.flip()
                # print("Click ", pos, "Grid coordinates: ", row, column)


## _______________________________________________________________ -------- Main Program Loop -----------__________________________________________________
while not done:
    for event in pygame.event.get():  # User did something

        #CLOSE
        if event.type == pygame.QUIT:
            done = True

        #KEY PRESSED
        elif event.type == pygame.KEYDOWN:
            #Escape key
            if event.key == pygame.K_ESCAPE:
                done = True

            #Ctrl+A pressed
            elif event.key == pygame.K_a:
                mods = pygame.key.get_mods()
                #If pressed ctrl+A keep making a wall until ctrl+Alt is pressed
                if mods & pygame.KMOD_CTRL:
                    makeWall()
                

            #Spacebar pressed FIND PATH FROM START TO END
            elif event.key == pygame.K_SPACE:
                
                if not FLAG:
                    continue
                else:
                    find_path(START_Co, END_Co)

        #SET_START_MARKER_ON_CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (GRID_WIDTH + GRID_MARGIN)
            row = pos[1] // (GRID_HEIGHT + GRID_MARGIN)
            x = (GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN
            y = (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN

            if len(START_xy) == 0:
                START_xy = (x, y)
                START_Co = (row, column)
            else:
                grid[START_Co[0]][START_Co[1]] = 1
                START_xy = (x, y)
                START_Co = (row, column)

            grid[row][column] = -1

        #SET_END_MARKER_ON_RELEASE
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (GRID_WIDTH + GRID_MARGIN)
            row = pos[1] // (GRID_HEIGHT + GRID_MARGIN)
            x = (GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN
            y = (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN

            if len(END_xy) == 0:
                END_xy = (x, y)
                END_Co = (row, column)
            else:
                grid[END_Co[0]][END_Co[1]] = 1
                END_xy = (x, y)
                END_Co = (row, column)

            grid[row][column] = -2
            print("done")
            FLAG = True

# Set the screen background
    screen.fill(BACKGROUND)

    # Draw the grid
    for row in range(GRID_ROWS):
        for column in range(GRID_COLUMNS):
            if grid[row][column] == -1:
                screen.blit(start_image, [START_xy[0], START_xy[1]])
            elif grid[row][column] == -2:
                screen.blit(end_image, [END_xy[0], END_xy[1]])
            else:
                color = GRID_COLOR
                if grid[row][column] == 0:
                    color = WALL_COLOR
                if grid[row][column] == 2:
                    color = TRAVERSAL_COLOR
                if grid[row][column] == 3:
                    color = PATH_COLOR
                #time.sleep(1)
                pygame.draw.rect(
                    screen, color,
                    [(GRID_MARGIN + GRID_WIDTH) * column + GRID_MARGIN,
                     (GRID_MARGIN + GRID_HEIGHT) * row + GRID_MARGIN,
                     GRID_WIDTH, GRID_HEIGHT])
# Limit to 60 frames per second
    clock.tick(20)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()