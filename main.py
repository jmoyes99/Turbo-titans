import pygame
from pygame.locals import *
import random
import time

pygame.init()

# Set name and variables
pygame.display.set_caption("Turbo Titans")
SPEED = 5
BACKGROUND_SPEED = 5
SCORE = 0

# Set screen info
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 650
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
FramePerSec = pygame.time.Clock()

# Defining colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Making fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("Road final.png")


class Hugh(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(250, SCREEN_WIDTH - 250), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED + 0.5)
        if (self.rect.bottom > 750):
            SCORE += 1
            self.rect.top = -50
            self.rect.center = (random.randint(250, SCREEN_WIDTH - 250), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Car.png")
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (450, 540)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 250:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-25, 0)
        if self.rect.right < SCREEN_WIDTH - 250:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(25, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('Road final.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingDownSpeed = BACKGROUND_SPEED + 1

    def update(self):
        self.bgY1 += self.movingDownSpeed
        self.bgY2 += self.movingDownSpeed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def render(self):
        SCREEN.blit(self.bgimage, (self.bgX1, self.bgY1))
        SCREEN.blit(self.bgimage, (self.bgX2, self.bgY2))


P1 = Player()
E1 = Hugh()

back_ground = Background()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:

    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()

    back_ground.update()
    back_ground.render()

    scores = font_small.render(str(SCORE), True, BLACK)
    SCREEN.blit(scores, (10, 10))

    # Moves and re-draws all Sprites
    for entity in all_sprites:
        SCREEN.blit(entity.image, entity.rect)
        entity.move()

    # If player and enemy collides the screen turns red and the game ends
    if pygame.sprite.spritecollideany(P1, enemies):
        SCREEN.fill(RED)
        SCREEN.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(0.5)
        pygame.quit()

    pygame.display.update()
    FramePerSec.tick(FPS)
