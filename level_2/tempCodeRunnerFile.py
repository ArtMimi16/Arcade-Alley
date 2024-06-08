import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1272, 705
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car")
BG = pygame.transform.scale(pygame.image.load("level_2/bg.jpg"), (WIDTH, HEIGHT))
fps = 60
white = [255, 255, 255]  # Correct color for white
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()
floor_img = pygame.image.load("level_2/floor.png")
floor_img = pygame.transform.scale(floor_img, (WIDTH, 50))  # Scale it if necessary
floor_height = floor_img.get_height()
floor_y = HEIGHT - floor_height
player_img = pygame.image.load("level_2/car.png")
player_img = pygame.transform.scale(player_img, (378, 164))  # Scale it if necessary
player_x = WIDTH // 2  # Initial x position
player_y = floor_y - player_img.get_height()

running = True

while running:
    timer.tick(fps)
    player = pygame.draw.rect(screen, white, [player_x, player_y, 20, 30])
    screen.blit(BG, (0, 0))
    screen.blit(floor_img, (0, floor_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5

    # Ensure the player stays within the screen boundaries
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_img.get_width():
        player_x = WIDTH - player_img.get_width()

    # Redraw the background
    screen.blit(BG, (0, 0))
    
    # Draw the floor image at the bottom of the screen
    screen.blit(floor_img, (0, floor_y))
    
    # Draw the player image
    screen.blit(player_img, (player_x, player_y))

    pygame.display.flip()

pygame.quit()
