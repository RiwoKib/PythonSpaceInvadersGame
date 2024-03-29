import pygame, pygame.mixer, math
from sys import exit
import random, time

#INITIALIZE & SETUP
pygame.mixer.init()
pygame.init()

opener = pygame.mixer.Sound('spaceinvaders/opener.wav')
play_shot = pygame.mixer.Sound('spaceinvaders/laser.wav')
play_explosion = pygame.mixer.Sound('spaceinvaders/explosion.wav')

CLOCK = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invader")
ICON = pygame.image.load('spaceinvaders/spaceship.png').convert()
pygame.display.set_icon(ICON)
game_active = False

pixel_font = pygame.font.Font('spaceinvaders/Pixeltype.ttf', 50)
SCORE_FONT = pygame.font.Font('spaceinvaders/Pixeltype.ttf',42)
GAME_OVER_FONT = pygame.font.Font('freesansbold.ttf',64)
BUTTON_TEXT_FONT = pygame.font.Font('spaceinvaders/Pixeltype.ttf',38)

#WORLD
BG = pygame.image.load("spaceinvaders/bg.jpg").convert()
BULLET = pygame.transform.scale(pygame.image.load('spaceinvaders/bullet.png'),(20,25)).convert_alpha()
ENEMY = pygame.image.load("spaceinvaders/enemy.png").convert_alpha()
PLAYER = pygame.image.load('spaceinvaders/invader.png').convert_alpha()

class Player(pygame.sprite.Sprite):

    def __init__(self, player_image):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom = (400,570))
        self.player_velocity = 10
        self.score_value = 0
        self.health = 100

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.player_velocity
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom + bar_height + 5 < SCREEN_HEIGHT:
            self.rect.y += self.player_velocity
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.player_velocity
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.player_velocity

    def display(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_image):
        super().__init__()
        self.image = enemy_image
        self.random_x_position = random.randint(10, SCREEN_WIDTH - 64)
        #random_y_position = random.randint(-40, 0)
        self.rect = self.image.get_rect(midtop = (self.random_x_position,0))
        self.enemy_speed = random.randint(1,3)
        self.enemy_angle = random.uniform(0, math.pi * 2)

    def update(self):
        self.rect.x += math.sin(self.enemy_angle) * self.enemy_speed
        self.rect.y += math.cos(self.enemy_angle) * self.enemy_speed

        if self.rect.right > SCREEN_WIDTH:
            self.enemy_angle *= -1
            self.rect.x += math.sin(self.enemy_angle) * self.enemy_speed
            self.rect.y += math.cos(self.enemy_angle) * self.enemy_speed

        if self.rect.left < 0:
            self.enemy_angle *= -1
            self.rect.x += math.sin(self.enemy_angle) * self.enemy_speed
            self.rect.y += math.cos(self.enemy_angle) * self.enemy_speed

        if self.rect.top < -64 or self.rect.bottom > SCREEN_HEIGHT + 64:
            self.kill()
            enemies.remove(self)

    def display(self, surface):
        surface.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, player_rect):
        super().__init__()
        self.image = bullet_image
        bullet_x = player_rect.x + (player_rect.width // 2)
        bullet_y = player_rect.y + (player_rect.height // 2)
        self.rect = self.image.get_rect(midbottom =(bullet_x + 5, bullet_y))
        self.bullet_velocity = 15


    def update(self):
        self.rect.y -= self.bullet_velocity

        if self.rect.top < 0:
            self.kill()
            bullets.remove(self)

    def display(self, surface):
        surface.blit(self.image, self.rect)



#CREATE THE PLAYER
player = Player(PLAYER)


#CREATE HEALTH BAR
bar_width = player.rect.width
bar_height = 5
bar_width_decrement = bar_width // player.health + 1

bar_color = {
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'orange': (255, 140, 0)
}


#WAIT FOR enemies/bullets/collisions
bullets = []
enemies = []
enemy_collided= []
enemy_bullet_collided = []
bullet_enemy_collided = []
enemy_shot = False

#ADD A USER EVENT to randomize enemy spawning
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1000)

# INCREASE_ENEMY_SPEED = pygame.USEREVENT + 1
# pygame.time.set_timer(INCREASE_ENEMY_SPEED, 5000)


#SPRITE GROUPS for collisions
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle(player)


#BUILDING BLOCKS
play_again_btn = pygame.Rect(230,320,150,50)
quit_btn = pygame.Rect(400, 320, 150, 50)

#HELPERS to show text to buttons
def text_objects(text,color):
	textsurface = BUTTON_TEXT_FONT.render(text,True,color)	

	return textsurface,textsurface.get_rect()	

def text_to_button(text,
                   color,
                   btnx,
                   btny,
                   btnw,
                   btnh):
	textsurface, textrect = text_objects(text,color)	
	textrect.center = (btnx+(btnw//2),btny+(btnh//2))
	SCREEN.blit(textsurface,textrect)


def intro_screen():
    global bar_width

    #RESET variables
    play_clicked = False
    bar_width = player.rect.width
    player.score_value = 0
    player.health = 100

    pygame.draw.rect(SCREEN,(0,0,255),play_again_btn,border_radius=15)
    pygame.draw.rect(SCREEN,(255,0,0),quit_btn, border_radius=15)

    #SHOW PLAY & QUIT text on their buttons
    text_to_button('PLAY', (255,255,255), 230,320,150,50)
    text_to_button('QUIT', (255,255,255), 400,320,150,50)
    
    #HANDLE BTN CLICKS
    mouse_pos = pygame.mouse.get_pos()

    if play_again_btn.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0] == 1 and not play_clicked:
            print('PLAY')
            play_clicked = True
            opener.play()
    elif quit_btn.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.quit()
            exit()
    
    if pygame.mouse.get_pressed()[0] == 0:
        play_clicked = False

    return play_clicked

def game_over_screen():
    game_over_text = GAME_OVER_FONT.render('GAME OVER',True,(255,255,255))
    SCREEN.blit(game_over_text, (200,250))

def draw_window():
    #SHOW SCORE
    score = SCORE_FONT.render('SCORE:' +str(player.score_value) , False, (64,64,64))
    score_rect = score.get_rect(bottomleft = (0,600))
    pygame.draw.rect(SCREEN, (255,182,193),score_rect)
    SCREEN.blit(score, score_rect)

    #SHOW BULLETS & MOVEMENTS
    bullet_group.update()
    bullet_group.draw(SCREEN)
    
    #SHOW ENEMIES & MOVEMENTS
    enemy_group.update()    
    enemy_group.draw(SCREEN)
    
    #SHOW & HANDLE PLAYER MOVEMENTS
    player_group.draw(SCREEN)
    player_group.update()

    #SHOW HEALTH BAR
    if player.health > 80:
        pygame.draw.rect(SCREEN, bar_color['green'], (bar_x, bar_y, bar_width, bar_height))
    elif player.health >= 50:
        pygame.draw.rect(SCREEN, bar_color['orange'], (bar_x, bar_y, bar_width, bar_height))
    elif player.health < 50:
        pygame.draw.rect(SCREEN, bar_color['red'], (bar_x, bar_y, bar_width, bar_height))

#THE GAME LOOP
while True:
    CLOCK.tick(60)
    
    #SHOW BACKGROUND
    SCREEN.blit(BG, (0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == SPAWN_ENEMY:
                enemy = Enemy(ENEMY)
                enemies.append(enemy)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_shot.play().set_volume(0.1)
                bullet = Bullet(BULLET, player.rect)
                bullets.append(bullet)

    #ADD BULLETS & ENEMIES to sprite groups
    for bullet in bullets:
        bullet_group.add(bullet)

    for enemy in enemies:
        enemy_group.add(enemy)
  
    #MOVE HEALTH BAR with player
    bar_x = player.rect.x
    bar_y = player.rect.y + player.rect.height


    #CHECK ENEMY collisions with bullet and player
    for enemy in enemies:
        enemy_bullet_collided = pygame.sprite.spritecollide(enemy, bullet_group, True, pygame.sprite.collide_mask)

        if enemy_bullet_collided:
            play_explosion.play().set_volume(0.1)
            enemies.remove(enemy)
            enemy_group.remove(enemy)
            player.score_value += 1 
            

        enemy_collided = pygame.sprite.collide_mask(player_group.sprite, enemy)

        if enemy_collided:
            enemies.remove(enemy)
            enemy_group.remove(enemy)  
            player.health -= 1  
            bar_width -= bar_width_decrement

    
    if bar_width < 0:
        enemy_group.empty()
        enemies.clear()
        bullet_group.empty()
        bullets.clear()
        game_active = False
        player.rect.midbottom = (400,570)

    if game_active:
        draw_window()
    else:
        if intro_screen():
            game_active = True
    
    pygame.display.flip()

