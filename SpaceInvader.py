import pygame, math
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
game_active = True


SCORE_FONT = pygame.font.Font('freesansbold.ttf',32)
GAME_OVER_FONT = pygame.font.Font('freesansbold.ttf',64)
BUTTON_TEXT_FONT = pygame.font.Font('freesansbold.ttf',18)

#WORLD
BG = pygame.image.load("spaceinvaders/bg.jpg").convert()

#SCORE VALUE
score_value = 0
score = SCORE_FONT.render('SCORE:' +str(score_value) , False, (64,64,64))
score_rect = score.get_rect(bottomleft = (0,600))

class Player(pygame.sprite.Sprite):

    def __init__(self,):
        super().__init__()
        self.PLAYER = pygame.image.load('spaceinvaders/invader.png').convert_alpha()
        self.rect = self.PLAYER.get_rect(midbottom = (400,570))
        self.player_velocity = 10

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.player_velocity
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.player_velocity
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.player_velocity
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.player_velocity

    def display(self, surface):
        surface.blit(self.PLAYER, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ENEMY = pygame.image.load("spaceinvaders/enemy.png").convert_alpha()
        self.random_x_position = random.randint(0, SCREEN_WIDTH)
        #random_y_position = random.randint(-40, 0)
        self.rect = self.ENEMY.get_rect(midtop = (self.random_x_position,0))
        self.enemy_speed = 0.01
        self.enemy_angle = 0

    def move(self):
        self.rect.x += math.sin(self.enemy_angle) * self.enemy_speed
        self.rect.y -= math.cos(self.enemy_angle) * self.enemy_speed

        if self.rect.right > SCREEN_WIDTH:
            self.enemy_angle *= -1
            self.rect.x += math.sin(self.enemy_angle) * self.enemy_speed
            self.rect.y -= math.cos(self.enemy_angle) * self.enemy_speed

        if self.rect.left < 0:
            self.enemy_angle *= -1
            self.rect.x += math.sin(self.enemy_angle) * self.enemy_speed
            self.rect.y -= math.cos(self.enemy_angle) * self.enemy_speed

    def display(self, surface):
        surface.blit(self.ENEMY, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.BULLET = pygame.image.load('spaceinvaders/bullet.png').convert_alpha()
        bullet_x = player_rect.x + (player_rect.width // 2)
        bullet_y = player_rect.y + (player_rect.height // 2)
        self.rect = self.BULLET.get_rect(midbottom =(bullet_x + 5, bullet_y))
        self.bullet_velocity = 15

    def fire_bullet(self):
        self.rect.y -= self.bullet_velocity

    def display(self, surface):
        surface.blit(pygame.transform.scale(self.BULLET, (20,25)), self.rect)


#CREATE THE PLAYER
player = Player()

#WAIT FOR ENEMIES & BULLETS
bullets = []
enemies = []

#ADD A USER EVENT to randomize enemy spawning
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 2000)


#SPRITE GROUPS for collisions
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


def collisions():
    '''handle collitions between player & enemy
        enemy & bullet'''
    
    if pygame.sprite.spritecollide(player, enemy_group, True):
        print('enemy collision!!')
    
    for bullet in bullets:
        if pygame.sprite.spritecollide(bullet, enemy_group, True):
            print('enemy shot')
            enemy_group.empty()


def draw_window():
    #SHOW BACKGROUND
    SCREEN.blit(BG, (0,0))

    #SHOW SCORE
    pygame.draw.rect(SCREEN, (255,182,193),score_rect)
    SCREEN.blit(score, score_rect)

    #SHOW BULLETS
    for bullet in bullets:
        bullet.display(SCREEN)
        bullet.fire_bullet()
        bullet_group.add(bullet)
    
    #SHOW & HANDLE PLAYER MOVEMENTS
    player.display(SCREEN)
    player.move()

    #SHOW ENEMIES & MOVEMENTS
    for enemy in enemies:
        enemy.display(SCREEN)
        enemy.move()
        enemy_group.add(enemy)
    
    
    collisions()



#THE GAME LOOP
while game_active:
    CLOCK.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == SPAWN_ENEMY:
            enemy = Enemy()
            enemy.enemy_speed = random.randint(1,2)
            enemy.enemy_angle = random.uniform(0, math.pi * 2)
            enemies.append(enemy)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect)
                bullets.append(bullet)

    draw_window()

    pygame.display.update()

