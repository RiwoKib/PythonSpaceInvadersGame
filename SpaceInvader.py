import pygame
from sys import exit

#INITIALIZE & SETUP
pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
ICON = pygame.image.load('spaceinvaders/spaceship.png').convert()
pygame.display.set_icon(ICON)
SCORE_FONT = pygame.font.Font('freesansbold.ttf',32)
GAME_OVER_FONT = pygame.font.Font('freesansbold.ttf',64)
BUTTON_TEXT_FONT = pygame.font.Font('freesansbold.ttf',18)
CLOCK = pygame.time.Clock()



#SCORE
score_value = 0

#WORLD
BG = pygame.image.load("spaceinvaders/bg.jpg").convert_alpha()
score = SCORE_FONT.render('SCORE:' +str(score_value) , False, 'black')

#PLAYER
PLAYER = pygame.image.load('spaceinvaders/invader.png').convert_alpha()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #SHOW BACKGROUND
    SCREEN.blit(BG, (0,0))


    #SHOW SCORE
    SCREEN.blit(score, (10,10))

    #SHOW PLAYER
    SCREEN.blit(PLAYER, (400, 520))

    pygame.display.update()
    CLOCK.tick(60)