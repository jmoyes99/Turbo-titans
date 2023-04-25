import pygame
from pygame.locals import *
import random
import time

pygame.init()

# Set Name and Variables
pygame.display.set_caption("Turbo Titans")
SPEED = 5
BACKGROUND_SPEED = 8
SCORE = 0

# Set Screen info
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 650
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
FramePerSec = pygame.time.Clock()

# Defining Colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (50, 255, 50)

# Making Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 50)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("Road final.png")
Enemy_image = pygame.image.load("Enemy.png")


# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = Enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(250, SCREEN_WIDTH - 250), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED + 0.5)
        if (self.rect.bottom > 750):
            SCORE += 1  # Adds Score
            self.rect.top = -50  # Resets Enemy 50 pixels above the Screen
            self.rect.center = (
                random.randint(250, SCREEN_WIDTH - 250), 0)  # Chooses Random point on the Road to spawn in

    # Blits Enemy Sprite onto Screen
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Playable Character Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Car.png")
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (450, 540)

    # Moves player according to keys pressed
    def move(self):
        # Allows player to move from left to right
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 250:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-25, 0)
        if self.rect.right < SCREEN_WIDTH - 250:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(25, 0)
        # Cheat button that allows player to go off the road
        if pressed_keys[K_ESCAPE]:
            global SCORE
            SCORE += 10
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-25, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(25, 0)

    # Blits player

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # Class for the Background


class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('Road final.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        pressed_keys = pygame.key.get_pressed()
        global BACKGROUND_SPEED

        if SCORE < 15:
            BACKGROUND_SPEED += 5

        self.movingDownSpeed = BACKGROUND_SPEED

    # Moves background according to the above variables
    def update(self):
        self.bgY1 += self.movingDownSpeed
        self.bgY2 += self.movingDownSpeed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    # Puts Background onto Screen
    def render(self):
        SCREEN.blit(self.bgimage, (self.bgX1, self.bgY1))
        SCREEN.blit(self.bgimage, (self.bgX2, self.bgY2))


P = Player()
E = Enemy()

back_ground = Background()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E)
all_sprites = pygame.sprite.Group()
all_sprites.add(P)
all_sprites.add(E)

# Adding a New User event
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

    # If player and enemy collides the screen turns blue and the game ends
    if pygame.sprite.spritecollideany(P, enemies):
        SCREEN.fill(BLUE)
        SCREEN.blit(game_over, (275, 280))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        pygame.quit()

    pygame.display.update()
    FramePerSec.tick(FPS)
