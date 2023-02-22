import pygame, sys
from pygame.locals import *

pygame.init()

screenWidth = 1024
screenHeight = 768

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Cursor")
pygame.mouse.set_visible(False)

while True:
    screen.fill((0,0,0))

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

    x, y = pygame.mouse.get_pos()
    
    pygame.draw.circle(screen, (255,0,0), (x, y), 20, 64)

    pygame.display.update()