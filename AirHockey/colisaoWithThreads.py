from typing import List
import pygame, sys
import math
from pygame.locals import *
import time
from random import randint
from threading import Thread
from classes.circulo import Circulo

def main():
    pygame.init()

    screenWidth = 1024
    screenHeight = 768
    raio_circulo = 20
    time_player = time.time()
    fps = 60
    x, y = pygame.mouse.get_pos()
    vely = 0
    velx = 0

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Cursor")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont('roboto', 40, True, True)

    player = Circulo(raio_circulo, x, y, 50)
    circle = Circulo(raio_circulo, randint(raio_circulo, screenWidth - raio_circulo), randint(raio_circulo, screenHeight - raio_circulo), 100)

    circulos = []
    circulos.append(circle)

    class Att_Pos_Worker(Thread):
        def __init__(self):
            Thread.__init__(self)

        def Att_Pos_Player(self):
            x, y = pygame.mouse.get_pos()
            time_now = time.time()

            dt = (time_now - player.tempo)

            if dt > 0:    
                mouse_velocity = math.sqrt((player.x - x)**2 + (player.y - y)**2) / dt
                mouse_velocity = mouse_velocity * fps
                #print(mouse_velocity)

                player.Att_Pos(x,y)
                player.Att_Vel(mouse_velocity)

        # Função com tipagem de parâmetro
        def Att_Circles(self, cirs: List[Circulo]):
            for c in cirs:
                time_now = time.time()
                c_x = c.x
                c_y = c.y

                if velx > 0:
                    c_x = c.x + velx
                if velx < 0:
                    c_x = c.x + velx
                if vely > 0:
                    c_y = c.y + vely
                if vely < 0:
                    c_y = c.y + vely

                dt = (time_now - c.tempo)

                if dt > 0:
                    c_velocity = math.sqrt((c.x - c_x)**2 + (c.y - c_y)**2) / dt
                    c_velocity = c_velocity
                    #print(c_velocity)

                    c.Att_Pos(c_x, c_y)
                    c.Att_Vel(c_velocity)

        def run(self):
            while True:
                self.Att_Pos_Player()
                self.Att_Circles(circulos)

    worker = Att_Pos_Worker()
    worker.daemon = True
    worker.start()

    while True:
        screen.fill((0,0,0))
        #clock.tick(fps)
    
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
    
        #Att_Pos_Player()
    
        circle_player = pygame.draw.circle(screen, (255,0,0), (player.x, player.y), player.raio, 64)
        for i in circulos:
            c = pygame.draw.circle(screen, (0,0,255), (i.x, i.y), i.raio, 64)
        
        #Att_Circles(circulos)
    
        pygame.display.update()

if __name__ == "__main__":
    main()