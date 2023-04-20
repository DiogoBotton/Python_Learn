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

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
fonte = pygame.font.SysFont("arial", 40, True, False)
#msg = "Aperte qualquer tecla para animar o sapinho :)"
#screen_txt = fonte.render(msg, True, WHITE)

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
        self.animate = False
        self.jumping = False
        
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


# Lista de todas as sprites que terão no game
allSprites = pygame.sprite.Group()
dino = Dino()
allSprites.add(dino)

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
    allSprites.draw(screen)
    allSprites.update()
    #screen.blit(screen_txt, (50, 50))
    pygame.display.flip()