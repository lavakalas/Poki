import pygame
from pygame.locals import *

import constants


pygame.init()
                   
font = pygame.font.SysFont('Droid Sans Monospace', 30)
vec = pygame.math.Vector2




BG_COLOR = (255, 255, 255)
ACC = 0.5
FRIC = -0.04
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FramesPerSecond = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


pygame.display.set_caption('Poki')


 
class SpriteSheet(object):
 
    def __init__(self, file_name):
 
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
 
 
    def get_image(self, x, y, width, height):

        image = pygame.Surface((width, height)).convert_alpha()


        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 

        return image
 

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((180, 120))
        #self.surf.fill((0, 204, 0))
        
        self.STATE = 'idle'  # idle run jump fall

        
        self.direction = 1 # 1 for right 0 for left
        self.animation_delay = 4
        self.delay_counter = 0
        self.frames = 10 # most common amount of frames for animations, starting with idle
        self.animation_frame = 0
        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect = self.surf.get_rect(center=(10, 485))
        self.spritesheets = [[SpriteSheet('asstes/knight/Colour1/NoOutline/120x80_PNGSheets/_Idle.png'), 10], 
        [SpriteSheet('asstes/knight/Colour1/NoOutline/120x80_PNGSheets/_Run.png'), 10], 
        [SpriteSheet('asstes/knight/Colour1/NoOutline/120x80_PNGSheets/_Jump.png'), 3],
        [SpriteSheet('asstes/knight/Colour1/NoOutline/120x80_PNGSheets/_Fall.png'), 3]]
        self.image = self.spritesheets[0][0].get_image(120 * self.animation_frame, 0, 120, 80)
        self.surf.blit(self.image, self.image.get_rect())
    

    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        self.acc = vec(0, 0.5)
        if self.STATE != 'jump' and self.STATE != 'fall':
                self.STATE = 'idle'
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            self.direction = 0
            if self.STATE != 'jump' and self.STATE != 'fall':
                self.STATE = 'run'
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.direction = 1
            if self.STATE != 'jump' and self.STATE != 'fall':
                self.STATE = 'run'
        if pressed_keys[K_SPACE]:
            self.jump()
            self.STATE = 'jump'
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + self.acc


        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        
        if self.STATE == 'jump' and self.vel.y > 0:
            self.STATE = 'fall'

        self.rect.midbottom = self.pos
    
    def update(self):
        collide = pygame.sprite.spritecollide(player, platforms, False)
        if collide:
            self.pos.y = collide[0].rect.top + 1
            self.vel.y = 0
            if self.STATE == 'jump' or self.STATE == 'fall':
                self.STATE = 'idle'
    def animate(self):
        
        if self.STATE == 'idle':
            self.image = self.spritesheets[0][0].get_image(120 * self.animation_frame, 0, 120, 80)
            self.frames = self.spritesheets[0][1]
        if self.STATE == 'run':
            self.image = self.spritesheets[1][0].get_image(120 * self.animation_frame, 0, 120, 80)
            self.frames = self.spritesheets[1][1]
        if self.STATE == 'jump':
            self.image = self.spritesheets[2][0].get_image(120 * self.animation_frame, 0, 120, 80)
            self.frames = self.spritesheets[2][1]
        if self.STATE == 'fall':
            self.image = self.spritesheets[3][0].get_image(120 * self.animation_frame, 0, 120, 80)
            self.frames = self.spritesheets[3][1]
        
        self.delay_counter += 1

        if self.delay_counter == self.animation_delay:
            self.delay_counter = 0
            self.animation_frame = (self.animation_frame + 1) % self.frames

        if self.direction == 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (180, 120))
        self.surf.blit(self.image, self.image.get_rect())
        self.surf.set_colorkey((0,0,0))
    
    def jump(self):
        collide = pygame.sprite.spritecollide(player, platforms, False)
        if collide:
            self.vel.y -= 15
    def data(self):
        return f"X:{format(self.pos.x, '.2f')} Y:{format(self.pos.y, '.2f')} Xvel:{format(self.vel.x, '.2f')} Yvel:{format(self.vel.y, '.2f')}"
        

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
sprites.add(player)

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
    player.animate()


    for entity in sprites:
        screen.blit(entity.surf, entity.rect)
        entity.move()

    screen.blit(text, (0, 0))

    print(player.STATE)
    pygame.display.update()

    FramesPerSecond.tick(FPS)

pygame.quit()