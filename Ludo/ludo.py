import pygame, sys
from math import floor
from pygame.locals import *
from random import randint
import time
from constants import *

pygame.init()

screenWidth = 900
screenHeight = screenWidth
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
                (5,4),(5,3),(5,2),(5,1),
                # Ways
                (6,1),(7,1),(7,2),(7,3),(7,4),(7,5)
            ]
gridReds = [
                (9,0),(9,1),(9,2),(9,3),(9,4),(9,5),
                (10,0),(11,0),(12,0),(13,0),(14,0),
                (14,5),(13,5),(12,5),(11,5),(10,5),
                (14,4),(14,3),(14,2),(14,1),
                # Ways
                (13,6),(13,7),(12,7),(11,7),(10,7),(9,7)
            ]
gridBlues = []
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
    pygame.draw.line(screen, DARKGREEN, (borderWidth - (borderWidth/2), 0), (borderWidth - (borderWidth/2), screenHeight), borderWidth)
    pygame.draw.line(screen, DARKGREEN, (0, borderWidth - (borderWidth/2)), (screenWidth, borderWidth - (borderWidth/2)), borderWidth)
    pygame.draw.line(screen, DARKGREEN, (screenWidth - (borderWidth/2), 0), (screenWidth - (borderWidth/2), screenHeight), borderWidth)
    pygame.draw.line(screen, DARKGREEN, (0, screenHeight - (borderWidth/2)), (screenWidth, screenHeight - (borderWidth/2)), borderWidth)
    # ---------------------------------------------------------------------------------------

    for x in range(0, squares+1):
        cordHorizontal = screenDraw_XY[0] + (gridPixels * x)
        pygame.draw.line(screen, BLACK, (screenDraw_XY[0], cordHorizontal), (screenDraw_XY[1], cordHorizontal)) # Draw Lines
        for y in range(0, squares+1):
            cordVertical = screenDraw_XY[0] + (gridPixels * y)
            pygame.draw.line(screen, BLACK, (cordVertical, screenDraw_XY[0]), (cordVertical, screenDraw_XY[1])) # Draw Lines

            if (x,y) in gridGreens: 
                pygame.draw.rect(screen,GREEN,(cordVertical, cordHorizontal,gridPixels,gridPixels))
            if (x,y) in gridReds: 
                pygame.draw.rect(screen,RED,(cordVertical, cordHorizontal,gridPixels,gridPixels))
            if (x,y) in gridOranges: 
                pygame.draw.rect(screen,ORANGE,(cordVertical, cordHorizontal,gridPixels,gridPixels))
            if (x,y) in gridBlues: 
                pygame.draw.rect(screen,BLUE,(cordVertical, cordHorizontal,gridPixels,gridPixels))

    pygame.display.update()