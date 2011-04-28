#! /usr/bin/python2.6

'''
The view for the CGOL implementation.
'''
import cgol

import sys
import time
import pygame
from pygame.locals import *



def draw_grid():
    for x in range(0, width, CELL_SIZE):
        for y in range(0, height, CELL_SIZE):
            r = pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            rects.append(r)
        
def get_index(position):
    x_pos = position[0]
    y_pos = position[1]
    column = x_pos / CELL_SIZE
    row = y_pos / CELL_SIZE
    return (column, row)
    
def get_rect(index):
    to_use = index[0] * GRID_SIZE[1] + index[1]
    return rects[to_use]
    
def add_to_dict(index):
    to_toggle = start_dict.setdefault(index, cgol.Cell())
    to_toggle.alive = not to_toggle.alive
    update_dict.setdefault(index, cgol.Cell())
    
def update_screen():
    for index, value in update_dict.items():
        r = get_rect(index)
        toggle_rect(r)
        to_update.append(r)
        
    pygame.display.update(to_update)
    
def toggle_rect(rect):
    x, y = rect.topleft
    col = screen.get_at((x + 1, y + 1))
    if col == pygame.Color(*BLUE):
        new_col = WHITE
    else:
        new_col = BLUE
    screen.fill(new_col, (x+1, y + 1, CELL_SIZE-2, CELL_SIZE-2))
    
        

CELL_SIZE = 10 #width and height of each cell, px
GRID_SIZE = (140, 80) #numbers of columns and rows for the entire grid
WHITE = (255, 255, 255, 255)
BLACK = (0,0,0, 255)
BLUE = (0,0,0, 255)

rects = []
to_update = []
update_dict = {}
start_dict = {}


size = width, height = CELL_SIZE * GRID_SIZE[0], CELL_SIZE * GRID_SIZE[1]
screen = pygame.display.set_mode(size) 
screen.fill(WHITE)
draw_grid()
pygame.display.flip()

clock = pygame.time.Clock()



running = True
going = False
pause = True

while running:

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT: 
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pause:
                index = get_index(event.pos)
                add_to_dict(index)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if not pause:
                start_dict = gr._grid.copy()
            pause = not pause
            if pause:
                going = not going
    
    if not pause and not going:
        gr = cgol.Grid(GRID_SIZE, start_dict.copy())
        going = True
        
    if going:
        update_dict= gr.step()
         
    update_screen()
    update_dict = {}    
    to_update = []
    clock.tick(250)
