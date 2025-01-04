import pygame, sys
import math
from pygame.locals import *
from random import randint
import time

pygame.init()

screenWidth = 1024
screenHeight = 768
raio_circulo = 20

c1_x = randint(raio_circulo, screenWidth - raio_circulo)
c1_y = randint(raio_circulo, screenHeight - raio_circulo)
c2_x = randint(raio_circulo, screenWidth - raio_circulo)
c2_y = randint(raio_circulo, screenHeight - raio_circulo)
#x, y = pygame.mouse.get_pos()
time_player = time.time()
fps = 60
x, y = screenWidth / 2, screenHeight / 2
vely = 0
velx = 0

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Cursor")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
circle_player = pygame.draw.circle(screen, (255,0,0), (x, y), raio_circulo, 64)

def detectar_colisao_circulos(origem, alvo):
    vetor_magnitude = math.sqrt((alvo.x - origem.x)**2 + (alvo.y - origem.y)**2)

    if vetor_magnitude <= (raio_circulo*2):
        print("colidiu")

while True:
    screen.fill((0,0,0))
    dt = clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_UP:
                vely -= 1
            if e.key == K_DOWN:
                vely += 1
            if e.key == K_RIGHT:
                velx += 1
            if e.key == K_LEFT:
                velx -= 1
    
    ball_velocity = math.sqrt((circle_player.centerx - x)**2 + (circle_player.centery - y)**2) / (time.time() - time_player)
    ball_velocity = ball_velocity * fps
    print(ball_velocity)

    #mouse_velocity = math.sqrt((x - pygame.mouse.get_pos()[0])**2 + (y - pygame.mouse.get_pos()[1])**2) / (time.time() - time_player)
    #mouse_velocity = mouse_velocity * fps

    #x, y = pygame.mouse.get_pos()
    time_player = time.time()
    
    if velx > 0:
        x = x + velx
    if velx < 0:
        x = x + velx
    if vely > 0:
        y = y + vely
    if vely < 0:
        y = y + vely

    circle_player = pygame.draw.circle(screen, (255,0,0), (x, y), raio_circulo, 64)
    circle_1 = pygame.draw.circle(screen, (0,0,255), (c1_x, c1_y), raio_circulo, 64)
    circle_2 = pygame.draw.circle(screen, (0,0,255), (c2_x, c2_y), raio_circulo, 64)

    circles = [circle_1, circle_2]

    for i in circles:
        detectar_colisao_circulos(circle_player, i)

    pygame.display.update()