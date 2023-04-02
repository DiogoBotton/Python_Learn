import pygame, sys
from math import floor
from pygame.locals import *
from random import randint
import time
from constants import *

pygame.init()

screenWidth = 700
screenHeight = 700
borderWidth = 15
squares = 15 # 15x15

screenDraw_XY = (borderWidth * 2, screenWidth - (borderWidth * 2))

gridPixels = (screenDraw_XY[1] - screenDraw_XY[0]) / squares

# Grids painted
# ------------------------------------------------------
gridGreens = [
                (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),
                (1,0),(2,0),(3,0),(4,0),(5,0),
                (5,5),(4,5),(3,5),(2,5),(1,5),
                (5,5),(4,5),(3,5),(2,5),(1,5),
                (5,4),(5,3),(5,2),(5,1),
                # Ways
                (6,1),(7,1),(7,2),(7,3),(7,4),(7,5)
            ]
gridBlues = []
gridReds = []
gridOranges = []
# ------------------------------------------------------

time_player = time.time()
fps = 60
x, y = screenWidth / 2, screenHeight / 2

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Ludo")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

while True:
    screen.fill((255,255,255))
    dt = clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

    # Borders
    # ---------------------------------------------------------------------------------------
    pygame.draw.line(screen, DARKGREEN, (0, 0), (0, screenHeight), borderWidth)
    pygame.draw.line(screen, DARKGREEN, (0, 0), (screenWidth, 0), borderWidth)
    pygame.draw.line(screen, DARKGREEN, (screenWidth, 0), (screenWidth, screenHeight), borderWidth)
    pygame.draw.line(screen, DARKGREEN, (0, screenHeight), (screenWidth, screenHeight), borderWidth)
    # ---------------------------------------------------------------------------------------

    for x in range(0, squares):
        cordHorizontal = screenDraw_XY[0] + (gridPixels * x)
        #pygame.draw.line(screen, BLACK, (screenDraw_XY[0], cordHorizontal), (screenDraw_XY[1], cordHorizontal))
        #pygame.draw.rect(screen,GREEN,(screenDraw_XY[0], cordHorizontal,gridPixels,gridPixels))
        for y in range(0, squares):
            cordVertical = screenDraw_XY[0] + (gridPixels * y)
            #pygame.draw.line(screen, BLACK, (cordVertical, screenDraw_XY[0]), (cordVertical, screenDraw_XY[1]))
            #pygame.draw.rect(screen,GREEN,(cordVertical, screenDraw_XY[0],gridPixels,gridPixels))
            if (x,y) in gridGreens: 
                pygame.draw.rect(screen,GREEN,(cordVertical, cordHorizontal,gridPixels,gridPixels))
            if (x,y) in gridReds: 
                pygame.draw.rect(screen,RED,(cordVertical, cordHorizontal,gridPixels,gridPixels))
            if (x,y) in gridOranges: 
                pygame.draw.rect(screen,ORANGE,(cordVertical, cordHorizontal,gridPixels,gridPixels))
            if (x,y) in gridBlues: 
                pygame.draw.rect(screen,BLUE,(cordVertical, cordHorizontal,gridPixels,gridPixels))

    pygame.display.update()