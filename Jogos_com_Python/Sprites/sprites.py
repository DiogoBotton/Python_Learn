import pygame, sys
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
fonte = pygame.font.SysFont("arial", 40, True, False)
msg = "Aperte qualquer tecla para animar o sapinho :)"
screen_txt = fonte.render(msg, True, WHITE)

pygame.display.set_caption("Importando Sprites")
clock = pygame.time.Clock()
fps = 60
scale = 4
spritesPerSec = 12
update_value = spritesPerSec/fps

# Classe sapo HERDA (Herança) da classe Sprite do pygame
class Sapo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.atual = 0
        for i in range(1,11):
            self.sprites.append(pygame.image.load(f"Sprites/attack_{i}.png"))
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width*scale, self.rect.height*scale))
        # Posiciona sapo no centro da tela
        self.rect.topleft = (screenWidth/2)-self.rect.width, (screenHeight/2)-self.rect.height*scale
        self.animar = False
    
    def atacar(self):
        self.animar = True
    
    def update(self):
        if not self.animar:
            return

        if self.atual >= len(self.sprites)-1:
            self.atual = 0
            self.animar = False

        self.atual += update_value
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (self.rect.width*scale, self.rect.height*scale))

sapo = Sapo()

# Lista de todas as sprites que terão no game
allSprites = pygame.sprite.Group()
allSprites.add(sapo)

while True:
    screen.fill(BLACK)
    dt = clock.tick(fps)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        if e.type == KEYDOWN:
            sapo.atacar()
            
    allSprites.draw(screen)
    allSprites.update()
    screen.blit(screen_txt, (50, 50))
    pygame.display.flip()