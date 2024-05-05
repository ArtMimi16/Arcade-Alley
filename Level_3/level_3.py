import pygame
from pygame.locals import *
import random
from pygame import mixer

pygame.init()

pygame.init()
mixer.music.load('hippogriff.mp3')
mixer.music.play(-1)

clock = pygame.time.Clock()
fps = 60

screen_width = 1272
screen_height = 705

player_width = 150
player_height = 132

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')


#define game variables
score = 0
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 270
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
font = pygame.font.SysFont(None, 55)


#load images
bg = pygame.image.load('bg.png')


class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.transform.scale(pygame.image.load(f'buckbeak{num}.png').convert_alpha(), (player_width, player_height))
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.mask = pygame.mask.from_surface(self.image)
		self.vel = 0
		self.clicked = False


	def update(self):

		if flying == True:
			#gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#handle the animation
			self.counter += 1
			flap_cooldown = 5

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			#rotate the bird
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index])



class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('tower.png')
		self.rect = self.image.get_rect()
		self.score_counted = False
		#position 1 is from the top, -1 is from the bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()



bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

run = True
while run:

	clock.tick(fps)

	#draw background
	screen.blit(bg, (0,0))

	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)

	#look for collision
	for bird in bird_group:
		for pipe in pipe_group:
			if pygame.sprite.collide_mask(bird, pipe):
				game_over = True
			elif pipe.rect.right < bird.rect.left and not pipe.score_counted:
				score += 0.5
				pipe.score_counted = True

	#check if bird has hit the ground
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False


	if game_over == False and flying == True:

		#generate new pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now


		#draw and scroll the ground
		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

		pipe_group.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	score_text = font.render(f'Score: {score}', True, (255, 255, 255))
	screen.blit(score_text, (10, 10))

	pygame.display.update()

pygame.quit()
