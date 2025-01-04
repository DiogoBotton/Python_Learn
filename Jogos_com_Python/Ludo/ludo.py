# JOGNA1 – Entrega N1.C
# Grupo 2: 
# Diogo Botton
# Felipe Katayama
# Kalli Yuka
# Leonardo Cardenas
# Wilian Barbosa

import pygame, sys
from pygame.locals import *
from random import randint
import time
from constants import *

screenWidth = int(input("Defina o tamanho da tela: "))
pygame.init()

screenHeight = screenWidth
borderWidth = 15
squares = 15 # 15x15

screenDraw_XY = (borderWidth * 2, screenWidth - (borderWidth * 2))

gridPixels = (screenDraw_XY[1] - screenDraw_XY[0]) / squares
centerXY = screenWidth / 2

# Grids painted
# ------------------------------------------------------
gridGreens = [
                (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),
                (1,0),(2,0),(3,0),(4,0),(5,0),
                (5,5),(4,5),(3,5),(2,5),(1,5),
                (5,4),(5,3),(5,2),(5,1),
                # Ways
                (6,1),(7,1),(7,2),(7,3),(7,4),(7,5),     
            ]
greenInside = [
                (2,2),(2,3),
                (3,2),(3,3)
            ]
gridReds = [
                (9,0),(9,1),(9,2),(9,3),(9,4),(9,5),
                (10,0),(11,0),(12,0),(13,0),(14,0),
                (14,5),(13,5),(12,5),(11,5),(10,5),
                (14,4),(14,3),(14,2),(14,1),
                # Ways
                (13,6),(13,7),(12,7),(11,7),(10,7),(9,7)
            ]
redInside = [
                (11,2),(11,3),
                (12,2),(12,3)
]
gridBlues = [
                (9,9),(9,10),(9,11),(9,12),(9,13),(9,14),
                (10,9),(11,9),(12,9),(13,9),(14,9),
                (14,14),(13,14),(12,14),(11,14),(10,14),
                (14,13),(14,12),(14,11),(14,10),
                # Ways
                (8,13),(7,13),(7,12),(7,11),(7,10),(7,9)
            ]
blueInside = [
                (11,11),(11,12),
                (12,11),(12,12)
                
]
gridOranges = [
                (0,9),(1,9),(2,9),(3,9),(4,9),(5,9),
                (0,9),(0,10),(0,11),(0,12),(0,13),(0,14),
                (1,14),(2,14),(3,14),(4,14),(5,14),
                (5,10),(5,11),(5,12),(5,13),(5,14),
                # Ways
                (1,8),(1,7),(2,7),(3,7),(4,7),(5,7)
            ]
orangeInside = [
                (2,11),(2,12),
                (3,11),(3,12)
]
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
        cordVertical = screenDraw_XY[0] + (gridPixels * x)
        pygame.draw.line(screen, BLACK, (screenDraw_XY[0], cordVertical), (screenDraw_XY[1], cordVertical)) # Draw Lines
        for y in range(0, squares+1):
            cordHorizontal = screenDraw_XY[0] + (gridPixels * y)
            pygame.draw.line(screen, BLACK, (cordHorizontal, screenDraw_XY[0]), (cordHorizontal, screenDraw_XY[1])) # Draw Lines

            if (x,y) in gridGreens: 
                pygame.draw.rect(screen,GREEN,(cordHorizontal, cordVertical,gridPixels,gridPixels))
            elif (x,y) in gridReds: 
                pygame.draw.rect(screen,RED,(cordHorizontal, cordVertical,gridPixels,gridPixels))
            elif (x,y) in gridOranges: 
                pygame.draw.rect(screen,ORANGE,(cordHorizontal, cordVertical,gridPixels,gridPixels))
            elif (x,y) in gridBlues: 
                pygame.draw.rect(screen,BLUE,(cordHorizontal, cordVertical,gridPixels,gridPixels))
            
            if (x,y) in greenInside:
                pygame.draw.rect(screen,GREEN,(cordHorizontal, cordVertical,gridPixels,gridPixels))
                pygame.draw.circle(screen, DARKGREEN, (cordHorizontal + (gridPixels/2), cordVertical + (gridPixels/2)), (gridPixels/3))
            elif (x,y) in redInside:
                pygame.draw.rect(screen,RED,(cordHorizontal, cordVertical,gridPixels,gridPixels))
                pygame.draw.circle(screen, RED2, (cordHorizontal + (gridPixels/2), cordVertical + (gridPixels/2)), (gridPixels/3))
            elif (x,y) in blueInside:
                pygame.draw.rect(screen,BLUE,(cordHorizontal, cordVertical,gridPixels,gridPixels))
                pygame.draw.circle(screen, BLUE2, (cordHorizontal + (gridPixels/2), cordVertical + (gridPixels/2)), (gridPixels/3))
            elif (x,y) in orangeInside:
                pygame.draw.rect(screen,ORANGE,(cordHorizontal, cordVertical,gridPixels,gridPixels))
                pygame.draw.circle(screen, ORANGE2, (cordHorizontal + (gridPixels/2), cordVertical + (gridPixels/2)), (gridPixels/3))

            if (x,y) == (6,6):
                pygame.draw.polygon(screen, GREEN,[(cordHorizontal, cordVertical), (centerXY, centerXY), (cordHorizontal, cordVertical + (gridPixels * 3))])
            elif (x,y) == (9,6):
                pygame.draw.polygon(screen, RED,[(cordHorizontal, cordVertical), (centerXY, centerXY), (cordHorizontal + (gridPixels * 3), cordVertical)])
            elif (x,y) == (9,9):
                pygame.draw.polygon(screen, BLUE,[(cordHorizontal, cordVertical), (centerXY, centerXY), (cordHorizontal, cordVertical - (gridPixels * 3))])
            elif (x,y) == (6,9):
                pygame.draw.polygon(screen, ORANGE,[(cordHorizontal, cordVertical), (centerXY, centerXY), (cordHorizontal - (gridPixels * 3), cordVertical)])

    pygame.display.update()