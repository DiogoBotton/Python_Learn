from threading import Thread
from typing import List
import pygame, sys
import math
from pygame.locals import *
import time
from random import randint
from classes.circulo import Circulo
from classes.retangulo import Retangulo

pygame.init()

screenWidth = 720
screenHeight = 768
raio_circulo = 30
time_player = time.time()
fps = 60
WHITE = (255,255,255)
rectangle_dimensions = (250, 50) #width, height
velXY_circle = 200
global initialize
initialize = False

global score
score = (0,0) # (player, oponent)

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Ping Pong")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
fonte = pygame.font.SysFont('roboto', 40, True, True)

player = Retangulo(rectangle_dimensions[0], rectangle_dimensions[1], (screenWidth / 2) - (rectangle_dimensions[0] / 2), screenHeight - 100, "bottom")
oponent = Retangulo(rectangle_dimensions[0], rectangle_dimensions[1], (screenWidth / 2) - (rectangle_dimensions[0] / 2), 50, "top")
circle = Circulo(raio_circulo, screenWidth / 2, screenHeight / 2)
mouse = Circulo(raio_circulo, screenWidth / 2, screenHeight / 2)

rectangles = []
rectangles.append(player)
rectangles.append(oponent)

def Att_Pos_mouse():
    x, y = pygame.mouse.get_pos()
    mouse.Att_Pos(x,y)

def RolarDados_Inicio():
    global initialize
    initialize = True

    value = randint(1, 100)
    value2 = randint(1, 100)

    if(value > 80):
        velx = velXY_circle if value2 < 60 else -velXY_circle
        vely = velXY_circle if value2 > 60 else -velXY_circle
    else:
        velx = -velXY_circle if value2 > 60 else +velXY_circle
        vely = -velXY_circle if value2 < 60 else +velXY_circle

    circle.Att_Vel_XY(velx, vely)

class Att_Pos_Worker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def detectar_colisao_bolinha(self, bolinha: Circulo):
        # Ao colidir com os limites da tela, inverte os eixos X ou Y
        # Colisão eixo X
        if (bolinha.x + raio_circulo) >= screenWidth or (bolinha.x + raio_circulo) <= (0 + raio_circulo*2):
            bolinha.Att_Vel_XY(-bolinha.velx, bolinha.vely)

        # Colisão eixo Y
        if (bolinha.y + raio_circulo) >= screenHeight or (bolinha.y + raio_circulo) <= (0 + raio_circulo*2):
            bolinha.Att_Vel_XY(0, 0)

        global score
        if (bolinha.y + raio_circulo) >= screenHeight:
            score = (score[0],score[1] +1)
            print("Oponente Pontuou")
        elif (bolinha.y + raio_circulo) <= (0 + raio_circulo*2):
            score = (score[0] +1, score[1])
            print("Player Pontuou")
        
        # Colisão com retângulos
        for r in rectangles:
            if(r.position.lower() == 'bottom'):
                  #                                         Eixo Y                                                    ///                                              Eixo X
                if((bolinha.y + raio_circulo) >= r.y and (bolinha.y + raio_circulo) <= r.y + rectangle_dimensions[1]) and (bolinha.x + raio_circulo) >= r.x and (bolinha.x - raio_circulo) <= r.x + rectangle_dimensions[0]:
                    bolinha.Att_Vel_XY(bolinha.velx, -bolinha.vely)
            else: 
                  #                                         Eixo Y                                                    ///                                              Eixo X
                if((bolinha.y - raio_circulo) >= r.y and (bolinha.y - raio_circulo) <= r.y + rectangle_dimensions[1]) and (bolinha.x + raio_circulo) >= r.x and (bolinha.x - raio_circulo) <= r.x + rectangle_dimensions[0]:
                    bolinha.Att_Vel_XY(bolinha.velx, -bolinha.vely)
    
    # Função com tipagem de parâmetro
    def Att_Pos_Rect(self, rects: List[Retangulo]):
        for r in rects:
            r_x = r.x
            local_fps = clock.get_fps() if clock.get_fps() != 0 else fps

            if r.velx > 0 and (r.x + rectangle_dimensions[0]) <= screenWidth:
                r_x = r.x + (r.velx / local_fps)
            if r.velx < 0 and (r.x + rectangle_dimensions[0]) >= rectangle_dimensions[0]:
                r_x = r.x + (r.velx / local_fps)
                
            r.Att_Pos(r_x)
    
    def Att_Pos_Ball(self, ball: Circulo):
        ball_x = ball.x
        ball_y = ball.y
        local_fps = clock.get_fps() if clock.get_fps() != 0 else fps

        if ball.velx > 0:
            ball_x = ball.x + (ball.velx / local_fps)
        if ball.velx < 0:
            ball_x = ball.x + (ball.velx / local_fps)
        if ball.vely > 0:
            ball_y = ball.y + (ball.vely / local_fps)
        if ball.vely < 0:
            ball_y = ball.y + (ball.vely / local_fps)
        
        if(ball.velx != 0 or ball.vely != 0):
            ball.Att_Pos(ball_x, ball_y)

    def run(self):
        while True:
            clock.tick(fps)
            self.Att_Pos_Rect(rectangles)
            self.Att_Pos_Ball(circle)
            self.detectar_colisao_bolinha(circle)

def main():
    worker = Att_Pos_Worker()
    worker.daemon = True
    worker.start()

    while True:
        screen.fill((0,0,0))

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()

        if(pygame.key.get_pressed()[K_RIGHT]):
            player.velx = 200
        elif(pygame.key.get_pressed()[K_LEFT]):
            player.velx = -200
        else:
            player.velx = 0

        ball = pygame.draw.circle(screen, WHITE, (circle.x, circle.y), circle.raio, 64)
        #mou = pygame.draw.circle(screen, WHITE, (mouse.x, mouse.y), mouse.raio, 64)

        #Att_Pos_mouse()

        player_retangulo = pygame.draw.rect(screen, WHITE, pygame.Rect(player.x, player.y, player.width, player.height))
        oponent_retangulo = pygame.draw.rect(screen, WHITE, pygame.Rect(oponent.x, oponent.y, oponent.width, oponent.height))

        if not initialize:
            RolarDados_Inicio()

        pygame.display.update()

if __name__ == "__main__":
    main()