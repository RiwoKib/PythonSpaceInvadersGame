import pygame
from sys import exit

#INITIALIZE & SETUP
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceinvaders/spaceship.png').convert()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


#WORLD
background = pygame.image.load("spaceinvaders/bg.jpg").convert()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)