import pygame, sys
from pygame.locals import *
import os

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Jump physic
Y_GRAVITY = 0.8
Y_SPINNING = 8
JUMP_HEIGHT = 15
Y_VELOCITY = JUMP_HEIGHT

screenWidth = 800
screenHeight = 600

# Armazena diretório principal onde o arquivo atual (Dino.py) esta armazenado
main_path = os.path.dirname(__file__)
# Armazena diretórios de som e imagens
img_path = os.path.join(main_path, 'images')
sounds_path = os.path.join(main_path, 'sounds')

pygame.init()
pygame.display.set_caption('Lontra Run')

screen = pygame.display.set_mode((screenWidth, screenHeight),0,32)
mainClock = pygame.time.Clock()
fps = 60

sprite_sheet = pygame.image.load(os.path.join(img_path, 'otter_moving.png')).convert_alpha() # convert_aplha mantem a transparência da imagem
sprite_sheet_iddle = pygame.image.load(os.path.join(img_path, 'otter_laugh.png')).convert_alpha()
resolution = 64 # Sprites com resolução de 64 x 64
scale = 3
spritesPerSecGame = 8
spritesPerSecMenu = 6
updateValueGame = spritesPerSecGame/fps
updateValueMenu = spritesPerSecMenu/fps
velx = 4
floorWidth = resolution*2
floor = screenHeight-150
lontraPosX = 150
 
font = pygame.font.SysFont(None, 20)

# Classe Lontra HERDA (Herança) da classe Sprite do pygame
class Lontra(pygame.sprite.Sprite):
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
        self.rect.center = (lontraPosX,floor)
        self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
        self.jumping = False
        self.running = False
    
    def set_menu(self):
        self.jumping = False
        self.running = False
        self.rect.center = (screenWidth-500,20)
        self.image = pygame.transform.scale(self.image, (resolution*8, resolution*8))

    def set_game(self):
        self.jumping = False
        self.running = True
        self.rect.center = (lontraPosX,floor)
        
    def update(self):
        if self.running:
            if self.index >= len(self.running_sprites)-1:
                self.index = 0

            self.index += updateValueGame
            self.image = self.running_sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
            
        # Calculo para simulação de física de pulo
        elif self.jumping:
            # Necessário global para conseguir referenciar variável
            global Y_VELOCITY
            self.rect.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY > Y_SPINNING:
                self.index = 0
            elif Y_VELOCITY <= 0:
                self.index = 3
            elif Y_VELOCITY <= Y_SPINNING:
                if self.index >= 2:
                    self.index = 0
                self.index += 1

            if Y_VELOCITY < -JUMP_HEIGHT and self.rect.center[1] >= floor:
                self.jumping = False
                self.running = True
                Y_VELOCITY = JUMP_HEIGHT
                self.rect.center = (lontraPosX,floor)

            self.image = self.jumping_sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
        else:
            if self.index >= len(self.iddle_sprites)-1:
                self.index = 0

            self.index += updateValueMenu
            self.image = self.iddle_sprites[int(self.index)]
            self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))

# Lista de todas as sprites que terão no game
allSprites = pygame.sprite.Group()
lontra = Lontra()
allSprites.add(lontra)
 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False
 
def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Lontra Ruunnn', font, (255, 255, 255), screen, 20, 20)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                lontra.set_game()
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
 
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
        
        lontra.set_menu()
        pygame.time.delay(2)
        allSprites.draw(screen)
        allSprites.update()

        pygame.display.flip()
        mainClock.tick(fps)
 
def game():
    running = True
    while running:
        screen.fill(WHITE)
        
        draw_text('game', font, BLACK, screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    lontra.set_menu()
                    running = False
        
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE]:
            lontra.jumping = True
            lontra.running = False

        pygame.time.delay(2)
        allSprites.draw(screen)
        allSprites.update()
        
        pygame.display.flip()
        mainClock.tick(fps)
 
def options():
    running = True
    while running:
        screen.fill(BLACK)
 
        draw_text('options', font, WHITE, screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.flip()
        mainClock.tick(fps)
 
main_menu()