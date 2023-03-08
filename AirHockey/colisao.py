from typing import List
import pygame, sys
import math
from pygame.locals import *
import time
from random import randint
from classes.circulo import Circulo

pygame.init()

screenWidth = 1024
screenHeight = 768
raio_circulo = 20
time_player = time.time()
fps = 60
x, y = pygame.mouse.get_pos()
vely = 0
velx = 0
coeficiente_atrito = 0.80
angulo_perpendicular = math.pi / 2

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Colisão")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
fonte = pygame.font.SysFont('roboto', 40, True, True)

player = Circulo(1, raio_circulo, x, y, 50)
circle = Circulo(2, raio_circulo, randint(raio_circulo, screenWidth - raio_circulo), randint(raio_circulo, screenHeight - raio_circulo), 100)
circle2 = Circulo(3, raio_circulo, randint(raio_circulo, screenWidth - raio_circulo), randint(raio_circulo, screenHeight - raio_circulo), 100)

circulos = []
circulos.append(circle)
circulos.append(circle2)

def reflexao(bolinha: Circulo):
    if bolinha.velx > 0 or bolinha.vely > 0:
        # multiplicando por 180 e dividindo por PI para converter de radianos para graus
        angulo_movimento = (math.atan2(bolinha.vely, bolinha.velx) * 180) / math.pi

        # Decompor velocidades
        velx = bolinha.velocidade * (math.cos(angulo_movimento * math.pi / 180))
        vely = bolinha.velocidade * (math.sin(angulo_movimento * math.pi / 180))

        angulo_incidencia = math.atan2(vely, velx)
        angulo_reflexao = (2 * angulo_incidencia) - angulo_perpendicular

        velx_novo = abs(bolinha.velx) * math.cos(angulo_reflexao)
        vely_novo = abs(bolinha.vely) * math.sin(angulo_reflexao)

        bolinha.Att_Vel_XY(velx_novo, vely_novo)

def atrito(bolinha: Circulo):
    if bolinha.velocidade > 0 and (bolinha.velx != 0 and bolinha.vely != 0):
        vx_final = -bolinha.velx * coeficiente_atrito
        vy_final = -bolinha.vely * coeficiente_atrito

        bolinha.Att_Vel_XY(vx_final, vy_final)
        #reflexao(bolinha)
        print("velX: ", vx_final, " velY: ", vy_final)

def detectar_colisao_parede(bolinha: Circulo):
    # Ao colidir com os limites da tela, inverte os eixos X ou Y
    # Colisão eixo X
    if (bolinha.x + raio_circulo) >= screenWidth or (bolinha.x + raio_circulo) <= (0 + raio_circulo*2):
        bolinha.Att_Vel_XY(-bolinha.velx, bolinha.vely)
        #atrito(bolinha)

    # Colisão eixo Y
    if (bolinha.y + raio_circulo) >= screenHeight or (bolinha.y + raio_circulo) <= (0 + raio_circulo*2):
        bolinha.Att_Vel_XY(bolinha.velx, -bolinha.vely)
        #atrito(bolinha)

def detectar_colisao_circulos(origem: Circulo, alvo: Circulo):
    distancia_x = alvo.x - origem.x
    distancia_y = alvo.y - origem.y
    distancia = math.sqrt((distancia_x)**2 + (distancia_y)**2)

    if distancia <= (raio_circulo*2):
        vel_colisao = alvo.velocidade - origem.velocidade
        velx_relativa = (alvo.velx - origem.velx)
        vely_relativa = (alvo.vely - origem.vely)
        
        normalX = velx / distancia
        normalY = vely / distancia
        velx_normal = velx_relativa * normalX
        vely_normal = vely_relativa * normalY
        velx_tangencial = velx_relativa - velx_normal
        vely_tangencial = vely_relativa - vely_normal

        v1_tang = (origem.velx * normalX) + (origem.vely * normalY), (origem.velx * -normalY) + (origem.vely * normalX)
        v2_tang = (alvo.velx * normalX) + (alvo.vely * normalY), (alvo.velx * -normalY) + (alvo.vely * normalX)

        v1_norm = ((origem.massa - alvo.massa) * velx_normal + 2 * alvo.massa * velx_normal) / (origem.massa + alvo.massa), ((origem.massa - alvo.massa) * vely_normal + 2 * alvo.massa * vely_normal) / (origem.massa + alvo.massa)
        v2_norm = ((alvo.massa - origem.massa) * velx_normal + 2 * origem.massa * velx_normal) / (origem.massa + alvo.massa), ((alvo.massa - origem.massa) * vely_normal + 2 * origem.massa * vely_normal) / (origem.massa + alvo.massa)

        v1_novo = (v1_tang[0] + v1_norm[0]), (v1_tang[1] + vel_colisao) 
        #v2_novo = (v2_tang[0] + v2_norm[0]), (v2_tang[1] + vel_colisao)
        v2y_novo = (alvo.velx * (alvo.massa - origem.massa) + 2 * origem.massa * origem.velx) / (origem.massa + alvo.massa)
        v2y_novo = (alvo.vely * (alvo.massa - origem.massa) + 2 * origem.massa * origem.vely) / (origem.massa + alvo.massa)

        origem.Att_Vel_XY(v1_novo[0], v1_novo[1])
        alvo.Att_Vel_XY(v2y_novo, v2y_novo)

        #print("colidiu")

def Att_Pos_Player():
    x, y = pygame.mouse.get_pos()
    time_now = time.time()

    dt =  (time_now - player.tempo)
        
    if dt > 0:
        mouse_velocity = math.sqrt((player.x - x)**2 + (player.y - y)**2) / dt
        #print(mouse_velocity)

        player.Att_Pos(x,y)
        player.Att_Vel(mouse_velocity)

# Função com tipagem de parâmetro
def Att_Circles(cirs: List[Circulo]):
    for c in cirs:
        time_now = time.time()
        c_x = c.x
        c_y = c.y
        local_fps = clock.get_fps() if clock.get_fps() != 0 else 1

        if c.velx > 0:
            c_x = c.x + (c.velx / local_fps)
        if c.velx < 0:
            c_x = c.x + (c.velx / local_fps)
        if c.vely > 0:
            c_y = c.y + (c.vely / local_fps)
        if c.vely < 0:
            c_y = c.y + (c.vely / local_fps)
        
        dt =  (time_now - c.tempo)
        
        if dt > 0:
            c_velocity = math.sqrt((c.x - c_x)**2 + (c.y - c_y)**2) / dt
            #print(c_velocity)

            c.Att_Pos(c_x, c_y)
            c.Att_Vel(c_velocity)

while True:
    screen.fill((0,0,0))
    clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_UP:
                circulos[0].vely -= 10
            if e.key == K_DOWN:
                circulos[0].vely += 10
            if e.key == K_RIGHT:
                circulos[0].velx += 10
            if e.key == K_LEFT:
                circulos[0].velx -= 10

    Att_Pos_Player()
    detectar_colisao_parede(player)

    circle_player = pygame.draw.circle(screen, (255,0,0), (player.x, player.y), player.raio, 64)

    # Cria todos os circulos e verifica colisões entre os mesmos
    for i in circulos:
        c = pygame.draw.circle(screen, (0,0,255), (i.x, i.y), i.raio, 64)
        detectar_colisao_circulos(player, i)
        detectar_colisao_parede(i)

        for x in range(0, (len(circulos) -1)):
            if i.id != circulos[x+1].id:
                detectar_colisao_circulos(i, circulos[x+1])
    
    Att_Circles(circulos)

    pygame.display.update()