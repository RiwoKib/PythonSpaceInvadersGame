import pygame 
import random
import math
from sys import exit

def show_score(x,y):
	score = score_font.render("Score: "+str(score_value),True,(255,255,255))
	win.blit(score,(x,y))

def text_objects(text,color,size="small"):
	if size == "small":
		textsurface = button_text_font.render(text,True,color)	

	return textsurface,textsurface.get_rect()	

def text_to_button(text,color,btnx,btny,btnw,btnh,size="small"):
	textsurface, textrect = text_objects(text,color,size)	
	textrect.center = (btnx+(btnw/2),btny+(btnh/2))
	win.blit(textsurface,textrect)

def game_over():
	game_over_text = game_over_font.render("GAME OVER",True,(255,255,255))
	win.blit(game_over_text,(200,250))
	pygame.mixer.music.stop()
	pygame.draw.rect(win,blue,(340,310,150,50))

	text_to_button("Play Again",white,340,310,150,50)

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if 340+150 > mouse[0] > 340 and 310+50 > mouse[1] > 310:
		pygame.draw.rect(win,dark_blue,(320,310,200,50))
		text_to_button("Play Again",white,340,310,150,50)
		if click[0] == 1:
			print("clicked")
	else:
		pygame.draw.rect(win,blue,(340,310,150,50))
		text_to_button("Play Again",white,340,310,150,50)

def player(x,y):
	win.blit(player_img,(x,y))


#initializing pygame
pygame.init()
win = pygame.display.set_mode((800,600)) 
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceinvaders/spaceship.png').convert()
pygame.display.set_icon(icon)
score_font = pygame.font.Font('freesansbold.ttf',32)
game_over_font = pygame.font.Font('freesansbold.ttf',64)
button_text_font = pygame.font.Font('freesansbold.ttf',18)
#background music
'''
pygame.mixer.music.load("spaceinvaders/background.wav")
pygame.mixer.music.play(-1)'''

#world
background = pygame.image.load("spaceinvaders/bg.jpg").convert()



#player
player_img = pygame.image.load('spaceinvaders/invader.png')
ply_x = 370
ply_y = 480
move_player = 0

#score
score_value = 0
textx = 10
texty =10


#play again button color and text
blue = (0,0,255)
dark_blue = (0,0,100)
white = (255,255,255)

#  multiple enemies
enemy_img = []
enmx = []
enmy = []
move_enemyx = []
move_enemyy = []
num_of_enemies = 6

for i in range(num_of_enemies) :
	enemy_img.append(pygame.image.load('spaceinvaders/enemy.png'))
	enmx.append(random.randint(0,735))
	enmy.append(random.randint(50,150))
	move_enemyx.append(3)
	move_enemyy.append(10)

def enemy(x,y):
	win.blit(enemy_img[i],(x,y))

#bullet
bullet_img = pygame.image.load('spaceinvaders/bullet.png')
bulty = 503
bultx = 0
bullet_state = "ready"
move_bulty = 5

def firebullet(x,y):
	global bullet_state
	bullet_state = "fire"
	win.blit(bullet_img,(x,y))

#collision
def iscollision(enmx,enmy,bultx,bulty):
	distance = math.sqrt(math.pow(enmx-bultx,2)+math.pow(enmy-bulty,2))

	if distance < 27:
		return True
	else:
		return False	


#game loop
run = True
while run:
	win.fill((0,0,0))
	win.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False		
			exit()

		#keyboard keys
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				move_player -= 0.5
			if event.key == pygame.K_RIGHT:
				move_player += 0.5
			if event.key == pygame.K_UP:
				if bullet_state == "ready":
					bullet_sound = pygame.mixer.Sound('spaceinvaders/laser.wav')
					bullet_sound.play()
					bultx = ply_x
					firebullet(bultx,bulty)
		if event.type == pygame.KEYUP:
			bultx = ply_x + 40
			firebullet(bultx,bulty)
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				move_player = 0 
				
	#borders		
	ply_x += move_player			
	if ply_x < 0: ply_x = 0 
	elif ply_x > 736: ply_x = 736

	#enemy movement
	for i in range(num_of_enemies):
		#game over
		if enmy[i] > 400:
			for j in range(num_of_enemies):
				enmy[j] = 2000
			run = game_over()	

		enmx[i] += move_enemyx[i]	
		if enmx[i] > 736:
			move_enemyx[i] -= 1
			enmy[i] += move_enemyy[i]
		elif enmx[i] < 0:
			move_enemyx[i] = 1
			enmy[i] += move_enemyy[i]

		#collision
		collision = iscollision(enmx[i],enmy[i],bultx,bulty)
		if collision:
			explosion_sound = pygame.mixer.Sound('spaceinvaders/explosion.wav')
			explosion_sound.play()
			bulty = 503
			bullet_state = "ready"
			score_value += 1
			enmx[i] = random.randint(0,735)
			enmy[i] = random.randint(50,150)		

		enemy(enmx[i],enmy[i])	

	#bullet movement
	if bullet_state == "fire":
		firebullet(bultx,bulty)
		bulty -= move_bulty
		if bulty < 0:
			bulty = 503
			bullet_state = "ready"

	player(ply_x,ply_y)
	show_score(texty,texty)
	pygame.display.update()		
