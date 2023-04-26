import random
import pygame, sys
from pygame.locals import *
from random import randrange
import os

# Armazena diretório principal onde o arquivo atual (Dino.py) esta armazenado
main_path = os.path.dirname(__file__)
# Armazena diretórios de som e imagens
img_path = os.path.join(main_path, 'images')
sounds_path = os.path.join(main_path, 'sounds')

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Jump physic
Y_GRAVITY = 0.8
JUMP_HEIGHT = 15
Y_VELOCITY = JUMP_HEIGHT

pygame.init()

# Em exceção da música de fundo, todos os outros sons deverão ser de extensão .WAV
sound_collide = pygame.mixer.Sound(os.path.join(sounds_path, 'death_sound.wav'))

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("Dino Game Sem Net")
clock = pygame.time.Clock()
fps = 60

sprite_sheet = pygame.image.load(os.path.join(img_path, 'dinoSpritesheet.png')).convert_alpha() # convert_aplha mantem a transparência da imagem
resolution = 32 # Sprites com resolução de 32 x 32
scale = 3
spritesPerSec = 12
updateValue = spritesPerSec/fps
velx = 4
floorWidth = resolution*2
floor = screenHeight-130
dinoPositionX = 150
score = 0

def draw_text(txt: str, size: int, color: tuple, xy: tuple):
    font = pygame.font.SysFont("comicsansms", size, True, False)
    msg = f"{txt}"
    textobj = font.render(msg, True, color)
    screen.blit(textobj, (xy[0],xy[1]))
    return textobj

# Classe Dino HERDA (Herança) da classe Sprite do pygame
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images_dino = []
        for i in range (0,3):
            # Seleciona seções especificas da imagem por coordenadas x y
            img = sprite_sheet.subsurface((resolution*i,0), (resolution,resolution))
            self.images_dino.append(img)
        
        self.index = 0
        self.image = self.images_dino[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (dinoPositionX,floor)
        self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))
        self.mask = pygame.mask.from_surface(self.image)
        self.animate = False
        self.jumping = False
        self.collided = False
        
    def update(self):
        if self.index >= len(self.images_dino)-1:
            self.index = 0
            self.animate = False

        self.index += updateValue
        self.image = self.images_dino[int(self.index)]
        self.image = pygame.transform.scale(self.image, (resolution*scale, resolution*scale))

        # Calculo para simulação de física de pulo
        if self.jumping:
            # Necessário global para conseguir referenciar variável
            global Y_VELOCITY
            self.rect.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY < -JUMP_HEIGHT and self.rect.center[1] >= floor:
                self.jumping = False
                Y_VELOCITY = JUMP_HEIGHT
                self.rect.center = (dinoPositionX,floor)

class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((resolution*7, 0), (resolution, resolution))
        self.image = pygame.transform.scale(self.image, (resolution*3, resolution*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50,200,50)
        self.rect.x = randrange(screenWidth,screenWidth + 320,80)
    
    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.y = randrange(50,200,50)
            self.rect.x = randrange(screenWidth,screenWidth + 320,80)
        self.rect.x -= velx

class Chao(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((resolution*6, 0), (resolution, resolution))
        self.image = pygame.transform.scale(self.image, (floorWidth, floorWidth))
        self.rect = self.image.get_rect()
        self.rect.y = screenHeight - 100
        self.rect.x = x * floorWidth
    
    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.x = screenWidth
        self.rect.x -= velx

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((resolution*5, 0), (resolution, resolution))
        self.image = pygame.transform.scale(self.image, (resolution*2, resolution*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (screenWidth, screenHeight - 100)

    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.center = (screenWidth, screenHeight - 100)
        
        self.rect.x -= velx

# Lista de todas as sprites que terão no game
allSprites = pygame.sprite.Group()
dinoSprites = pygame.sprite.Group()
obstaclesSprites = pygame.sprite.Group()

dino = Dino()
cacto = Cacto()
obstaclesSprites.add(cacto)
dinoSprites.add(dino)

for i in range(0,4):
    nuvem = Nuvem()
    allSprites.add(nuvem)

for i in range(screenWidth*2//floorWidth):
    chao = Chao(i)
    allSprites.add(chao)

while True:
    screen.fill(WHITE)
    dt = clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
    
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        dino.jumping = True

    pygame.time.delay(2)
    dinoSprites.draw(screen)
    allSprites.draw(screen)
    obstaclesSprites.draw(screen)

    # Colisão de sprites:
    # 1° paramêtro: sprite principal
    # 2° paramêtro: sprites que poderam se chocar com a principal
    # 3° paramêtro: se a sprite que colidiu com o dino será removida após a colisão (doKill)
    # 4° paramêtro: "FLAG", tipo da colisão, colisão de circulos, quadrados ou pixels (máscara)
    colisoes = pygame.sprite.spritecollide(dino, obstaclesSprites, False, pygame.sprite.collide_mask)

    # Caso houver uma colisão, libera aúdio de colisão e para de atualizar as sprites
    if colisoes and not dino.collided:
        sound_collide.play()
        dino.collided = True
    elif dino.collided:
        pass
    else:
        score += 1/2
        dinoSprites.update()
        allSprites.update()
        obstaclesSprites.update()
    
    draw_text(f'SCORE: {int(score)}', 40, BLACK, (screenWidth - (screenWidth-50), 50))
    pygame.display.flip()