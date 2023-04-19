# JOGNA1 – Entrega N1.D
# Grupo 2: 
# Diogo Botton
# Felipe Katayama
# Kalli Yuka
# Leonardo Cardenas
# Wilian Barbosa

import pygame, sys
from pygame.locals import *

# Edit the filename for desire file
filename = "Exercises_Python/dados1.txt"
file = open(filename, "r")

line = file.readline().replace("\n", "").split("|")
screenWidth = int(line[0])
screenHeight = int(line[1])
screen = pygame.display.set_mode((screenWidth, screenHeight))

line = file.readline().replace("\n", "").split("|")
BACKGROUND = (int(line[0]), int(line[1]), int(line[2]))

linesForDraw = []

for l in file:
    line = l.replace("\n", "").split("|")
    x_init = int(line[0])
    y_init = int(line[1])
    x_end = int(line[2])
    y_end = int(line[3])
    R = int(line[4])
    G = int(line[5])
    B = int(line[6])
    line_width = int(line[7])

    line_tuple = ((R,G,B), (x_init, y_init), (x_end, y_end), line_width)
    linesForDraw.append(line_tuple)

file.close()

pygame.display.set_caption("ExN1D")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
fps = 60

while True:
    screen.fill(BACKGROUND)
    dt = clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
    
    for i in linesForDraw:
        pygame.draw.line(screen, i[0], i[1], i[2], i[3]) # Draw Lines

    pygame.display.update()