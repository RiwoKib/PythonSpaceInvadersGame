import pygame
from sys import exit
import random

#INITIALIZE & SETUP
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invader")
ICON = pygame.image.load('spaceinvaders/spaceship.png').convert()
pygame.display.set_icon(ICON)


SCORE_FONT = pygame.font.Font('freesansbold.ttf',32)
GAME_OVER_FONT = pygame.font.Font('freesansbold.ttf',64)
BUTTON_TEXT_FONT = pygame.font.Font('freesansbold.ttf',18)

#SCORE VALUE
score_value = 0

#WORLD
BG = pygame.image.load("spaceinvaders/bg.jpg").convert()
score = SCORE_FONT.render('SCORE:' +str(score_value) , False, (64,64,64))
score_rect = score.get_rect(bottomleft = (0,600))

class Player(pygame.sprite.Sprite):

    def __init__(self,):
        super().__init__()
        self.PLAYER = pygame.image.load('spaceinvaders/invader.png').convert_alpha()
        self.player_rect = self.PLAYER.get_rect(midbottom = (400,570))
        self.player_velocity = 5

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            self.player_rect.y -= self.player_velocity
        if pressed_keys[pygame.K_DOWN] and self.player_rect.height + self.player_rect.y + self.player_velocity < SCREEN_HEIGHT:
            self.player_rect.y += self.player_velocity
        if pressed_keys[pygame.K_LEFT] and self.player_rect.x - self.player_velocity > 0:
            self.player_rect.x -= self.player_velocity
        if pressed_keys[pygame.K_RIGHT] and self.player_rect.x + self.player_rect.width + self.player_velocity < SCREEN_WIDTH:
            self.player_rect.x += self.player_velocity

    def display(self, surface):
        surface.blit(self.PLAYER, self.player_rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ENEMY = pygame.image.load("spaceinvaders/enemy.png").convert_alpha()
        self.random_x_position = random.randint(0, SCREEN_WIDTH)
        #random_y_position = random.randint(-40, 0)
        self.enemy_rect = self.ENEMY.get_rect(midtop = (self.random_x_position,0))
        self.enemy_vel = 2

    def move(self):
        self.enemy_rect.x += self.enemy_vel

        if self.enemy_rect.right > SCREEN_WIDTH:
            self.enemy_rect.left = -20

    def display(self, surface):
        surface.blit(self.ENEMY, self.enemy_rect)




#CREATE PLAYER & ENEMY
player = Player()
enemies = []

#ADD A USER EVENT to randomize enemy spawning
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 2000)



def draw_window():
    #SHOW BACKGROUND
    SCREEN.blit(BG, (0,0))

    #SHOW SCORE
    pygame.draw.rect(SCREEN, (255,182,193),score_rect)
    SCREEN.blit(score, score_rect)

    #SHOW & HANDLE PLAYER MOVEMENTS
    player.display(SCREEN)
    player.move()

    #SHOW ENEMIES & MOVEMENTS

    for enemy in enemies:
        enemy.display(SCREEN)
        enemy.move()

#THE GAME LOOP
while True:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == SPAWN_ENEMY:
            enemy = Enemy()
            enemies.append(enemy)

    draw_window()

    pygame.display.update()