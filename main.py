import pygame
from pygame.locals import *




pygame.init()
                   
font = pygame.font.SysFont('Droid Sans Monospace', 30)
vec = pygame.math.Vector2


BG_COLOR = (50, 50, 50)
ACC = 0.5
FRIC = -0.02
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FramesPerSecond = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Poki')
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((0, 204, 0))
        self.rect = self.surf.get_rect(center=(10, 385))
        
        self.STATE = 'idle'  # idle run jump midJump fall

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        idle_sprite = pygame.image.load('asstes/knight/Colour1/NoOutline/120x80_PNGSheets/_Idle.png').convert_alpha()
    

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        self.acc = vec(0, 0.5)

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        if pressed_keys[K_SPACE]:
            self.jump()
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + self.acc


        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos
    
    def update(self):
        collide = pygame.sprite.spritecollide(player, platforms, False)
        if collide:
            self.pos.y = collide[0].rect.top + 1
            self.vel.y = 0
    
    def jump(self):
        collide = pygame.sprite.spritecollide(player, platforms, False)
        if collide:
            self.vel.y -= 15
    def data(self):
        return f"X:{format(self.pos.x, '.2f')} Y:{format(self.pos.y, '.2f')} Xvel:{format(self.vel.x, '.2f')} Yvel:{format(self.vel.y, '.2f')}"
    
    def render(self):
        screen.blit(self.surf, self.rect)
        

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, 20))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))
    def move(self):
        pass

player = Player()
ground = Platform()

running = True


sprites = pygame.sprite.Group()
sprites.add(ground)

platforms = pygame.sprite.Group()
platforms.add(ground)


while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False   

    screen.fill(BG_COLOR)

    text = font.render(player.data(), False, (0, 178, 0))

    player.update()


    for entity in sprites:
        screen.blit(entity.surf, entity.rect)
    player.move()
    player.render()

    screen.blit(text, (0, 0))

    pygame.display.update()

    FramesPerSecond.tick(FPS)

pygame.quit()