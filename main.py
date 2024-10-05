"""
Plan:
use numpy array to represent every square of cubes
the moving piece not in numpy array but added on
once there's sth under the moving piece, STOP
when it stop, moving piece added
then check if there's a line that can be cleared, SO CLEAR IT and move all lines
for each piece his color, color stored in dict, (e.g. {0:"yellow", 1:"red",2:"blue",3:"green", ...})
speed up in each level for dynamics

pieces:
- I
- O
- S
- Z
- L
- J
- T
Why this project:
I want to start freelancing but didn't code for 3 months, so I try to get back to coding

don't worry if it's not like the original, it would be even better !
"""


import pygame
import numpy as np
import random
import time

SCREEN_SIZE = (1280, 720)
COLORS = {
    1:"blue", 
    2:"red", 
    3:"green", 
    4:"yellow",
    5:"cyan",
    6:"magenta",
    7:"maroon"
}

PIECES = { #x,y
    1:((-1,0),(0,0),(1,0),(2,0)), #I
    2:((0,0),(0,1),(1,0),(1,1)), #O
    3:((0,0),(0,1),(1,0),(-1,1)), #S
    4:((0,0),(0,1),(-1,0),(1,1)), #Z
    5:((0,0),(-1,0),(1,0),(-1,1)), #L
    6:((0,0),(-1,0),(1,0),(1,1)), #J
    7:((0,0),(-1,0),(1,0),(0,1)) #T
    #6:((0,0),(0,1),(-1,1))
}
NPIECES = tuple(PIECES.keys())
SCREEN_COLOR = "darkgray"
CUBE_SIZE = 30
GRID_CUBE_SIZE = (10,20) #x,y
GRID_COLOR = "black"
CUBES_LIMIT_COLOR = "white"
GRID_POS = (0,0) #x,y
NUMBER_NEXT_PIECES = 3
DELAY_CONTROL_H = 0.1 # to go left or right
DELAY_CONTROL_V = 0.1 # to go down

def flip_coords(x,y):
    """convert UI coords to numpy coords"""
    return y,x
def setup_current_piece():
    global cpiece_id, cpiece_pos, cpiece_cubes, grid
    
    #remove full lines
    for nline in range(GRID_CUBE_SIZE[1]):
        if np.all(grid[nline]):
            grid = np.delete(grid,nline,axis=0)
            #print(cubes)
            grid = np.vstack((empty_line, grid))
            #print(grid)
            pass
        
    cpiece_id = next_pieces.pop(0)
    next_pieces.append(random.choice(NPIECES))
    cpiece_pos = [int(GRID_CUBE_SIZE[0])//2, 0] #x,y
    cpiece_cubes = PIECES[cpiece_id]
    add_cpiece_to_grid()

def add_cpiece_to_grid():
    global cubes_w_cpiece
    grid_w_cpiece_cache = grid.copy()
    for cube in cpiece_cubes:
        cube_pos = cpiece_pos[0]+cube[0], cpiece_pos[1]+cube[1]
        if not (0<=cube_pos[0]<GRID_CUBE_SIZE[0] and 0<=cube_pos[1]<GRID_CUBE_SIZE[1]): # verif if it cross limits
            return False
        # if not 0<=cube_pos[0]<10:
        #     cpiece_pos[0] -= moving_h #cancel the move
        if grid_w_cpiece_cache[flip_coords(*cube_pos)]: # verif for conflicts
            return False
        grid_w_cpiece_cache[flip_coords(*cube_pos)] = cpiece_id
    cubes_w_cpiece = grid_w_cpiece_cache
    return True
    
def move_v(delta_v):
    cpiece_pos[1] += delta_v
    if not add_cpiece_to_grid(): # the piece finally placed
        cpiece_pos[1] -= delta_v
        
        global moving_v
        moving_v = 0
        global grid
        grid = cubes_w_cpiece
        
        #remove lines !
        setup_current_piece()

# def adjust_cpiece_pos():
#     global cpiece_pos
#     while True:
#         cubes_pos = []
#         for cube in cpiece_cubes:
#             cube_pos = cpiece_pos[0]+cube[0], cpiece_pos[1]+cube[1]
#             if cube_pos[0]<0:
#                 cpiece_pos
#     zpiece_cubes = tuple(zip(cpiece_cubes))
#     cpiece_pos = (
#         cpiece_pos[0] + min(zpiece_cubes[0]),
#         cpiece_pos[1] + min(zpiece_cubes[1])
#     )
grid = np.zeros(flip_coords(*GRID_CUBE_SIZE))
#cubes = array = np.random.randint(0, 5, size=GRID_CUBE_SIZE)
cube_surfaces = {}
for piece_id, color in COLORS.items():
    cube_surface = pygame.Surface((CUBE_SIZE, CUBE_SIZE))
    cube_surface.fill(color)
    cube_surfaces[piece_id] = cube_surface
    
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

running = True
next_pieces = [random.choice(NPIECES) for _ in range(NUMBER_NEXT_PIECES)]
if 1:
    pass
    #next_pieces[0] = 7
    
setup_current_piece()

empty_line = np.zeros((1,GRID_CUBE_SIZE[0]))
delay_moving = 1
next_time_moving = time.time()
next_time_moving_h = 0
next_time_moving_v = 0
moving_h = 0
moving_v = 0
next_time_moving += delay_moving
#adjust_cpiece_pos()
# Create grid_surface
grid_surface = pygame.Surface((GRID_CUBE_SIZE[0]*CUBE_SIZE, GRID_CUBE_SIZE[1]*CUBE_SIZE))
grid_surface.fill(GRID_COLOR)
for y in range(GRID_CUBE_SIZE[1]):
    pygame.draw.line(
        grid_surface,
        CUBES_LIMIT_COLOR,
        (0,y*CUBE_SIZE),
        (GRID_CUBE_SIZE[0]*CUBE_SIZE,y*CUBE_SIZE),
        1)
for x in range(GRID_CUBE_SIZE[0]):
    pygame.draw.line(
        grid_surface,
        CUBES_LIMIT_COLOR,
        (x*CUBE_SIZE,0),
        (x*CUBE_SIZE,GRID_CUBE_SIZE[1]*CUBE_SIZE),
        1)
while running:
    screen.fill(SCREEN_COLOR)
    screen.blit(grid_surface,GRID_POS)

    if time.time() > next_time_moving:
        next_time_moving += delay_moving
        move_v(1)
        
    if moving_h and time.time() > next_time_moving_h:
        next_time_moving_h += DELAY_CONTROL_H
        cpiece_pos[0] += moving_h
        if not add_cpiece_to_grid():
            cpiece_pos[0] -= moving_h # cancel the h move
            moving_h = 0
        
    if moving_v and time.time() > next_time_moving_v:
        print(next_time_moving_v)
        next_time_moving_v += DELAY_CONTROL_V
        #cpiece_pos[1] += moving_v
        move_v(moving_v)
        

        
    for y in range(GRID_CUBE_SIZE[1]):
        for x in range(GRID_CUBE_SIZE[0]):
            piece_id = cubes_w_cpiece[flip_coords(x,y)]
            if piece_id != 0:
                cube_surface = cube_surfaces[piece_id]
                screen.blit(cube_surface, (CUBE_SIZE*x+GRID_POS[0], CUBE_SIZE*y+GRID_POS[1]))
        
        # pygame.draw.line(
        #     screen, 
        #     "white", 
        #     (GRID_POS[0],CUBE_SIZE*y+GRID_POS[1]), 
        #     (GRID_POS[1]+GRID_CUBE_SIZE[1]*CUBE_SIZE,CUBE_SIZE*y+GRID_POS[1]), 
        #     1)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running=False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_time_moving_h = time.time()
                moving_h = -1
            elif event.key == pygame.K_RIGHT:
                next_time_moving_h = time.time()
                moving_h = 1
            elif event.key == pygame.K_DOWN:
                next_time_moving_v = time.time()
                moving_v = 1
            elif event.key == pygame.K_UP: # turn the piece
                cpiece_cubes_backup = cpiece_cubes
                cpiece_cubes = tuple((cube[1], -cube[0]) for cube in cpiece_cubes)
                if not add_cpiece_to_grid():
                    cpiece_cubes = cpiece_cubes_backup
                pass

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                moving_h = 0
                
            elif event.key == pygame.K_DOWN:
                moving_v = 0
    clock.tick(60) # fps
    pygame.display.flip()
            
pygame.quit()