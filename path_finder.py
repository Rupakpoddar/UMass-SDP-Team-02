from Sensors import *
import pygame
from movements import *

'''
# Initialize bme280
mySensor = qwiic_bme280.QwiicBme280()

if mySensor.connected == False:
    print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
'''  

# Initialize Pygame
pygame.init()

# Set grid size
maze_size = 25
cell_size = 25
GRID_ROWS = maze_size
GRID_COLUMNS = maze_size
start = [19,12]
                                                                                                                                                                                                                                
# Set the window size
window_size = (maze_size * cell_size, maze_size * cell_size)
screen = pygame.display.set_mode(window_size)

l_limit = r_limit = 5
f_limit = 19
turn = 2.25
fw = 1.4

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (69,139,116)
BANANA = (227,207,87)
RED = (255,48,48)

def draw():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLUMNS):
            if duct[row][col] == 0:
                color = WHITE
            elif duct[row][col] == 2:
                color = GREEN
            elif duct[row][col] == 3:
                color = BANANA
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, GRAY, (col * cell_size, row * cell_size, cell_size, cell_size), 1)
    
    #pygame.time.Clock().tick(2)
    pygame.display.flip()

def grid(start):
    global duct
    duct = [[0 for y in range(GRID_COLUMNS)] for x in range(GRID_ROWS)]
    x = start[1]
    y = start[0]
    #print(x,y)
    duct[y][x] = 2
    
def printGrid():
    for row in duct:
        print(row)
        
def moves():
    getProxValues()
    ret = ""
    side = ""
    
    if (values[3] < l_limit and values[4] < l_limit):
        print("left")
        turnLeft(turn)
        side = "right"
        #autoOrient("right")		#use right side as reference
        ret = 3
        
    elif (values[1] < r_limit and values[1] < r_limit) and values[0] > f_limit:
        print("right")
        turnRight(turn)
        side = "left"
        #autoOrient("left")		#use left side as reference
        ret = 1
    
    elif values[0] > f_limit:
        #print(values[0])
        print("uturn")
        autoOrient()
        turnRight(turn)
        turnRight(turn)
        autoOrient()
        ret = 2
    
    getProxValues()
    if (values[3] < l_limit and values[4] < l_limit) and (values[1] < r_limit and values[1] < r_limit) and side!="":
        print("forward")
        forward(fw)
        autoOrient(side)
    else:
        autoOrient(side)
        if values[0] < f_limit:
            print("forward")
            forward(fw)
            getProxValues()
            if (values[3] < l_limit or values[4] < l_limit) or (values[1] < r_limit or values[1] < r_limit):
                pass
            else:
                autoOrient()
        
            if ret == "":
                ret = 0
    return ret

def main():
    global duct
    
    grid(start)
    #printGrid()
    print("\n")
    curr = [0,0]
    curr[0], curr[1] = start[0], start[1]
    autoOrient()
    dir = 0
    i = 0
    while(i<30):
    
        move = moves()		#input("give input ")#moves()
        if move!="":
            
            getDiag(curr)
            ret = move
            move = (move+dir)%4
            temp = curr
            if move == 3:
                # left
                curr[1] -= 1
            elif move == 1:
                # right
                curr[1] += 1
            elif move == 2:
                # down
                curr[0] += 1
            elif move == 0:
                # up
                curr[0] -= 1
            
            dir = move
            if curr[0] < GRID_COLUMNS and curr[1] < GRID_ROWS:
                if ret == 2:
                    duct[temp[0]][temp[1]] = 3
                elif duct[curr[0]][curr[1]] == 2 or duct[curr[0]][curr[1]] == 3:
                    pass
                else:
                    duct[curr[0]][curr[1]] = 1
            else:
                print("out of bounds")
                curr = temp
        draw()
        
        if curr == start:
            print(curr, start)
            stop(0.1)
            print("starting point reached")
            break
        i+=1
    graph()   
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    # Quit Pygame
    pygame.quit()
main()


