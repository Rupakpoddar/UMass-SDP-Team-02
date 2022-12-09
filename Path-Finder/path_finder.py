import pygame, sys
from typing import Tuple

# Initialize pygame
pygame.init()

# Define colors
PATH_COLOR = (15, 250, 223)
TRAVERSAL_COLOR = (0, 0, 204)
BACKGROUND = (74, 71, 71)
GRID_COLOR = (0, 0, 0)
WALL_COLOR = (255, 0, 0)

# Set the WIDTH and HEIGHT of the screen
GRID_COLUMNS = 70
GRID_ROWS = 30

GRID_ITEM_WIDTH = 20
GRID_ITEM_HEIGHT = 20
GRID_ITEM_MARGIN = 2

WINDOW_SIZE = [
    GRID_COLUMNS * (GRID_ITEM_WIDTH + GRID_ITEM_MARGIN),
    GRID_ROWS * (GRID_ITEM_HEIGHT + GRID_ITEM_MARGIN),
]

screen = pygame.display.set_mode(WINDOW_SIZE)

# Load images
s_image = pygame.image.load("./start.png").convert_alpha()
start_image = pygame.transform.scale(s_image, (GRID_ITEM_WIDTH, GRID_ITEM_HEIGHT))

# end image
e_image = pygame.image.load("./end.png").convert_alpha()
end_image = pygame.transform.scale(e_image, (GRID_ITEM_WIDTH, GRID_ITEM_HEIGHT))

# _____________________________________MAKE MATRIX_______________________________________________________________
grid = [[1 for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
parent = [[None for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
start = None
end = None

pygame.display.set_caption("Array Backed Grid")


def get_xy_from_grid_coord(row: int, column: int) -> Tuple[int, int]:
    x = (GRID_ITEM_WIDTH + GRID_ITEM_MARGIN) * column + GRID_ITEM_MARGIN
    y = (GRID_ITEM_HEIGHT + GRID_ITEM_MARGIN) * row + GRID_ITEM_MARGIN

    return (x, y)


def draw_board():
    # Draw the grid
    screen.fill(BACKGROUND)

    for row in range(GRID_ROWS):
        for column in range(GRID_COLUMNS):
            if grid[row][column] == -1:
                screen.blit(start_image, list(get_xy_from_grid_coord(*start)))
            elif grid[row][column] == -2:
                screen.blit(end_image, list(get_xy_from_grid_coord(*end)))
            else:
                color = GRID_COLOR
                if grid[row][column] == 0:
                    color = WALL_COLOR
                if grid[row][column] == 2:
                    color = TRAVERSAL_COLOR
                if grid[row][column] == 3:
                    color = PATH_COLOR

                x, y = get_xy_from_grid_coord(row, column)
                pygame.draw.rect(
                    screen,
                    color,
                    [
                        x,
                        y,
                        GRID_ITEM_WIDTH,
                        GRID_ITEM_HEIGHT,
                    ],
                )

    pygame.time.Clock().tick(2)
    pygame.display.flip()


def find_path(start, goal):
    """
    start: start grid coordinate
    end: end grid coordinate

    grid[row][col]:
        -1: start
        -2: end
        0: wall
        1: unvisited node
        2: visited node
        3: path
    """

    queue = [start]

    # Up; Down; Left; Right
    available_directions = [(-1, 0), (+1, 0), (0, +1), (0, -1)]

    while len(queue) != 0:
        curr_node = queue.pop()
        curr_node_row, curr_node_col = curr_node

        if curr_node == goal:
            while curr_node != start:
                curr_node_row, curr_node_col = curr_node
                grid[curr_node_row][curr_node_col] = 3
                curr_node = parent[curr_node_row][curr_node_col]
            break

        for available_direction_row, available_direction_col in available_directions:
            target_row = curr_node_row + available_direction_row
            if target_row < 0 or target_row > GRID_ROWS:
                continue

            target_col = curr_node_col + available_direction_col
            if target_col < 0 or target_col > GRID_COLUMNS:
                continue

            # Skip walls
            if grid[target_row][target_col] == 0:
                continue

            # Skip visited nodes
            if grid[target_row][target_col] == 2:
                continue

            target = (target_row, target_col)
            queue.append(target)
            parent[target_row][target_col] = curr_node
            grid[target_row][target_col] = 2

            draw_board()


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
                    """
                    modsCtrl = pygame.key.get_mods()
                    if modsCtrl & pygame.KMOD_ALT:
                        WALL = False
                        break
                    """
            elif eventCtrl.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (GRID_ITEM_WIDTH + GRID_ITEM_MARGIN)
                row = pos[1] // (GRID_ITEM_HEIGHT + GRID_ITEM_MARGIN)

                # Set that location to one
                grid[row][column] = 0

                pygame.draw.rect(
                    screen,
                    WALL_COLOR,
                    [
                        (GRID_ITEM_WIDTH + GRID_ITEM_MARGIN) * column
                        + GRID_ITEM_MARGIN,
                        (GRID_ITEM_HEIGHT + GRID_ITEM_MARGIN) * row + GRID_ITEM_MARGIN,
                        GRID_ITEM_WIDTH,
                        GRID_ITEM_HEIGHT,
                    ],
                )
                pygame.display.flip()


## _______________________________________________________________ -------- Main Program Loop -----------__________________________________________________
while True:
    for event in pygame.event.get():
        # CLOSE
        if event.type == pygame.QUIT:
            pygame.quit()

        # KEY PRESSED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            # CTRL + A -- Make Wall
            if event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                makeWall()

            elif event.key == pygame.K_SPACE:
                if start is not None and end is not None:
                    find_path(start, end)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Set start marker on left click
            if event.button == 1:
                x, y = pygame.mouse.get_pos()

                row = y // (GRID_ITEM_HEIGHT + GRID_ITEM_MARGIN)
                column = x // (GRID_ITEM_WIDTH + GRID_ITEM_MARGIN)

                if start is not None:
                    # Remove the previous marker
                    grid[start[0]][start[1]] = 1

                start = (row, column)
                grid[row][column] = -1
            # Set end marker on right click
            elif event.button == 3:
                x, y = pygame.mouse.get_pos()

                row = y // (GRID_ITEM_HEIGHT + GRID_ITEM_MARGIN)
                column = x // (GRID_ITEM_WIDTH + GRID_ITEM_MARGIN)

                if end is not None:
                    # Remove the previous marker
                    grid[end[0]][end[1]] = 1

                end = (row, column)
                grid[row][column] = -2

    draw_board()
