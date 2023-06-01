import math
from random import randrange
import pygame, sys
from pygame.locals import *
import os

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Jump physic
Y_GRAVITY = 0.8
Y_SPINNING = 8
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

# Inicialização PyGame
pygame.init()
pygame.display.set_caption('Otter Run')

# Screen Resolution
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight),0,32)

# Armazena diretório principal onde o arquivo atual (otterRun.py) esta armazenado
main_path = os.path.dirname(__file__)

# Armazena diretórios de som e imagens
img_path = os.path.join(main_path, 'images')
sounds_path = os.path.join(main_path, 'sounds')

# Definição dos frames por segundo
mainClock = pygame.time.Clock()
fps = 60

# Sprites and Grounds
sprite_sheet = pygame.image.load(os.path.join(img_path, 'otter_moving.png')).convert_alpha() # convert_aplha mantem a transparência da imagem
sprite_sheet_iddle = pygame.image.load(os.path.join(img_path, 'otter_laugh.png')).convert_alpha()
sprite_sheet_obstacles = pygame.image.load(os.path.join(img_path, 'obstacles.png')).convert_alpha()
ground_img = pygame.image.load(os.path.join(img_path, 'ground_tile.png')).convert_alpha()
bg_menu = pygame.image.load(os.path.join(img_path, 'bg_menu.png')).convert_alpha()
bg_menu = pygame.transform.scale(bg_menu, (screenWidth, screenHeight))
bt_play = pygame.image.load(os.path.join(img_path, 'bt_play.png')).convert_alpha()
bt_exit = pygame.image.load(os.path.join(img_path, 'bt_exit.png')).convert_alpha()

# Variáveis necessárias
resolution = 64 # Sprites com resolução de 64 x 64
scale = 3 # Escala para ampliação de imagens
spritesPerSecGame = 4 # Sprites por segundo no game
spritesPerSecMenu = 3 # Sprites por segundo no menu

# Valor utilizado para exibir exatamente o número de sprites definidas nas variáveis acima
updateValueGame = spritesPerSecGame*2/fps
updateValueMenu = spritesPerSecMenu*2/fps

# Posição do chão em y e da otter em x
ground_y = screenHeight-172
otterPos_x = 150
ground_width = 320
ground_heigth = 32

# Velocidade em que se move os objetos
scroll = 1
valueObstacles = 320

# Pontuação
score = 0
increaseSpeedByScore = 250 # A cada X pontos aumenta velocidade
increaseValue = 0.1

font = pygame.font.SysFont('comicsansms', 35)

# Classes
# -----------------------------------------------------------------------
class Background():
    def __init__(self, x, image):
        self.x = x
        self.image = image
        self.velx = 0

# Classe Otter e Obstacles herdam (Herança) da classe Sprite do pygame
class Otter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.iddle_sprites = []
        self.running_sprites = []
        self.jumping_sprites = []
        for i in range (0,12):
            # Seleciona seções especificas da imagem por coordenadas x y
            img = sprite_sheet_iddle.subsurface((resolution*i,0), (resolution,resolution))
            self.iddle_sprites.append(img)
        for i in range (1,5):
            # Seleciona seções especificas da imagem por coordenadas x y
            img = sprite_sheet.subsurface((resolution*i,0), (resolution,resolution))
            self.running_sprites.append(img)
        for i in range (5,9):
            # Seleciona seções especificas da imagem por coordenadas x y
            img = sprite_sheet.subsurface((resolution*i,0), (resolution,resolution))
            self.jumping_sprites.append(img)
        
        self.index = 0
        self.image = self.running_sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (otterPos_x,ground_y)
        self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
        self.mask = pygame.mask.from_surface(self.image)
        self.jumping = False
        self.running = False
        self.collided = False
    
    def set_menu(self):
        self.jumping = False
        self.running = False
        self.rect.center = (screenWidth-520,screenHeight-320)
        self.image = pygame.transform.scale(self.image, (resolution*5, resolution*5))

    def set_game(self):
        self.jumping = False
        self.running = True
        self.collided = False
        self.rect.center = (otterPos_x,ground_y)
        
    def update(self):
        if self.running:
            if self.index >= len(self.running_sprites)-1:
                self.index = 0

            self.index += updateValueGame
            self.image = self.running_sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
            
        elif self.jumping:
            # Calculo para simulação de física de pulo
            # Necessário global para conseguir referenciar variável
            global Y_VELOCITY
            self.rect.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY

            # Alterna entre os sprites baseado na altura (y)
            if Y_VELOCITY > Y_SPINNING:
                self.index = 0
            elif Y_VELOCITY <= 0:
                self.index = 3
            elif Y_VELOCITY <= Y_SPINNING:
                if self.index >= 2:
                    self.index = 0
                self.index += 1

            if Y_VELOCITY < -JUMP_HEIGHT and self.rect.center[1] >= ground_y:
                self.jumping = False
                self.running = True
                Y_VELOCITY = JUMP_HEIGHT
                self.rect.center = (otterPos_x,ground_y)

            self.image = self.jumping_sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
        else: 
            # Menu
            if self.index >= len(self.iddle_sprites)-1:
                self.index = 0

            self.index += updateValueMenu
            self.image = self.iddle_sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))

class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range (0,4):
            img = sprite_sheet_obstacles.subsurface((resolution*i,0), (resolution,resolution))
            self.sprites.append(img)   
        self.reposition()
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        if self.rect.topright[0] <= 0:
            self.reposition()
        self.rect.x -= scroll*4
    
    def reposition(self):
        distIncrease = increaseValue*4
        self.image = self.sprites[randrange(0,4)]
        self.image = pygame.transform.scale(self.image, (resolution*2, resolution*2))
        self.rect = self.image.get_rect()
        self.rect.center = (randrange(screenWidth + (valueObstacles * distIncrease), screenWidth + valueObstacles + (valueObstacles * distIncrease)*4,80),screenHeight-(resolution+12))

class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_img
        self.image = pygame.transform.scale(self.image, (ground_width, ground_heigth))
        self.rect = self.image.get_rect()
        self.rect.y = screenHeight - ground_heigth
        self.rect.x = x * ground_width
    
    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.x = screenWidth
        self.rect.x -= scroll*4
# -----------------------------------------------------------------------
# Classes End

# Adquire todos os backgrounds e adiciona-os numa lista
bg_images = []
for i in range(1,3):
    bgImg = pygame.transform.scale(pygame.image.load(os.path.join(img_path, f'bg_{i}.png')).convert_alpha(), (screenWidth, screenHeight))
    bg = Background(0, bgImg)
    bg_images.append(bg)
bg_width = bg_images[0].image.get_width()

# Listas de todas as sprites que terão no game
otterSprites = pygame.sprite.Group()
obstaclesSprites = pygame.sprite.Group()
allOtherSprites = pygame.sprite.Group()
otter = Otter()
obstacles = Obstacles()
otterSprites.add(otter)
obstaclesSprites.add(obstacles)

for i in range(screenWidth*4//ground_width):
    ground = Ground(i)
    allOtherSprites.add(ground)

# Função para exibir backgrounds
def draw_bg():
    speed = 1
    for bg in bg_images:
        # Para cada img, cria +1 para o efeito background infinito
        for x in range(0,2):
            bg.velx += scroll
            bg.x = bg_width * x - (bg.velx * speed)
            screen.blit(bg.image, (bg.x, 0))
            
            if x > 0 and bg.x <= 0:
                bg.velx = 0
        speed += 0.2

# Função para exibir texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Função para pausar o jogo
def stop_game():
    global scroll
    scroll = 0

# Função para reiniciar o jogo
def reset_game():
    global scroll, score
    scroll = 1
    score = 0
    obstacles.reposition()
 
click = False
 
def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Otter Ruunnn', font, BLACK, screen, 20, 20)
        screen.blit(bg_menu, (0,0))
        mx, my = pygame.mouse.get_pos()
        
        global click
        button_1 = screen.blit(bt_play, (50,50))
        button_2 = screen.blit(bt_exit, (50,140))
        if button_1.collidepoint((mx, my)):
            if click:
                otter.set_game()
                reset_game()
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                exit()
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        otter.set_menu()
        pygame.time.delay(2)
        otterSprites.draw(screen)
        otterSprites.update()

        pygame.display.flip()
        mainClock.tick(fps)
 
def game():
    running = True
    while running:
        screen.fill(WHITE)

        global score
        draw_bg()
        draw_text(f'SCORE: {int(score)}', font, WHITE, screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    otter.set_menu()
                    running = False
        
        keys_pressed = pygame.key.get_pressed()
        global Y_VELOCITY
        if keys_pressed[pygame.K_SPACE]:
            if Y_VELOCITY <= 0 and Y_VELOCITY >= -8 and otter.jumping:
                Y_VELOCITY += 0.5
            otter.jumping = True
            otter.running = False

        pygame.time.delay(2)
        otterSprites.draw(screen)
        obstaclesSprites.draw(screen)
        allOtherSprites.draw(screen)

        colisoes = pygame.sprite.spritecollide(otter, obstaclesSprites, False, pygame.sprite.collide_mask)

        if colisoes and not otter.collided:
            otter.collided = True
            stop_game()
        elif otter.collided:
            draw_text('Game Over', font, WHITE, screen, screenWidth/3, screenHeight/2)
            draw_text('Aperte ESC para voltar ao menu', font, WHITE, screen, screenWidth/3, (screenHeight/2)+60)
            pass
        else:
            score += 1/2
            otterSprites.update()
            obstaclesSprites.update()
            allOtherSprites.update()
        
        if score % increaseSpeedByScore == 0:
            global scroll
            scroll += increaseValue
        
        pygame.display.flip()
        mainClock.tick(fps)
 
def exit():
    pygame.quit()
    sys.exit()
 
main_menu()