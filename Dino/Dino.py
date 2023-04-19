import pygame, sys
from pygame.locals import *
import os

# Armazena diretório principal onde o arquivo atual (Dino.py) esta armazenado
main_path = os.path.dirname(__file__)
# Armazena diretórios de som e imagens
img_path = os.path.join(main_path, 'images')
sounds_path = os.path.join(main_path, 'sounds')


BLACK = (0,0,0)
WHITE = (255,255,255)

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
        self.rect.center = (screenWidth/2,screenHeight/2)
        self.image = pygame.transform.scale(self.image, (self.rect.width*scale, self.rect.height*scale))
        self.animate = False

    def update(self):
        if self.index >= len(self.images_dino)-1:
            self.index = 0
            self.animate = False

        self.index += updateValue
        self.image = self.images_dino[int(self.index)]
        self.image = pygame.transform.scale(self.image, (self.rect.width*scale, self.rect.height*scale))

dino = Dino()

# Lista de todas as sprites que terão no game
allSprites = pygame.sprite.Group()
allSprites.add(dino)

while True:
    screen.fill(WHITE)
    dt = clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
            
    allSprites.draw(screen)
    allSprites.update()
    #screen.blit(screen_txt, (50, 50))
    pygame.display.flip()