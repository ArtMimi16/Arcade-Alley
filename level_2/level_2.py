import pygame
import random
from pygame import mixer

pygame.init()
mixer.music.load('level_2/basilisk.mp3')
mixer.music.play(-1)

WIDTH, HEIGHT = 1272, 705
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car")
BG = pygame.transform.scale(pygame.image.load("level_2/bg.jpg"), (WIDTH, HEIGHT))
fps = 60
white = [255, 255, 255]
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

# Load the floor image
floor_img = pygame.image.load("level_2/floor.png")
floor_img = pygame.transform.scale(floor_img, (WIDTH, 50))  # Scale it if necessary
floor_height = floor_img.get_height()
floor_y = HEIGHT - floor_height

# Load the player images
car_img = pygame.image.load("level_2/car.png")
car_img = pygame.transform.scale(car_img, (330, 182))  # Scale it if necessary

car_duck_img = pygame.image.load("level_2/car2.png")
car_duck_img = pygame.transform.scale(car_duck_img, (330, 100))  # Scale it if necessary

player_x = WIDTH // 4  # Initial x position (quarter way across screen)
player_y = floor_y - car_img.get_height()  # Initial y position to be on the floor

# Initialize floor scrolling
floor_x1 = 0
floor_x2 = WIDTH
floor_speed = 8

# Jumping variables
is_jumping = False
jump_speed = 20
gravity = 0.5
player_y_velocity = 0

# Load obstacle images
ground_obstacle_img = pygame.image.load("level_2/basilisk.png")
ground_obstacle_img = pygame.transform.scale(ground_obstacle_img, (192, 131))  # Scale if necessary

air_obstacle_img = pygame.image.load("level_2/spider.png")
air_obstacle_img = pygame.transform.scale(air_obstacle_img, (319, 628))  # Scale if necessary

class Obstacle:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
     
    def move(self, speed):
        self.x -= speed
        if self.x < -self.rect.width:
            return False  # Indicates the obstacle should be removed
        self.rect.topleft = (self.x, self.y)
        return True
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# List to hold obstacles
obstacles = []

# Obstacle generation timer
obstacle_timer = 0

running = True

while running:
    timer.tick(fps)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_y_velocity = -jump_speed
            elif event.key == pygame.K_DOWN:
                # Change the player image to the duck image
                car_img = car_duck_img
                # Adjust the player's y-coordinate so it touches the floor
                player_y = floor_y - car_duck_img.get_height()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                # Change the player image back to the regular car image
                car_img = pygame.image.load("level_2/car.png")
                car_img = pygame.transform.scale(car_img, (330, 182))
                # Reset the player's y-coordinate to be on the floor
                player_y = floor_y - car_img.get_height()

    # Apply gravity
    if is_jumping:
        player_y += player_y_velocity
        player_y_velocity += gravity

    # Ensure the player lands on the floor
    if player_y > floor_y - car_img.get_height():
        player_y = floor_y - car_img.get_height()
        is_jumping = False

    # Move the floor
    floor_x1 -= floor_speed
    floor_x2 -= floor_speed

    # Wrap the floor image around
    if floor_x1 <= -WIDTH:
        floor_x1 = WIDTH
    if floor_x2 <= -WIDTH:
        floor_x2 = WIDTH

    # Generate new obstacles
    obstacle_timer += 0.5
    if obstacle_timer >= 60:  # Adjust the timer for desired obstacle frequency
        obstacle_timer = 0
        if random.choice([True, False]):  # Randomly choose between ground and air obstacles
            new_obstacle = Obstacle(ground_obstacle_img, WIDTH, floor_y - ground_obstacle_img.get_height())
        else:
            new_obstacle = Obstacle(air_obstacle_img, WIDTH, floor_y - air_obstacle_img.get_height() - 100)
        obstacles.append(new_obstacle)

    # Move and draw obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle.move(floor_speed)]
    
    # Check for collisions
    player_rect = car_img.get_rect(topleft=(player_x, player_y))
    player_mask = pygame.mask.from_surface(car_img)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle.rect):
            # Perform pixel-perfect collision detection
            offset = (obstacle.rect.left - player_rect.left, obstacle.rect.top - player_rect.top)
            if player_mask.overlap(obstacle.mask, offset):
                print("Collision detected!")
                running = False

    # Redraw the background
    screen.blit(BG, (0, 0))
    
    # Draw the floor images
    screen.blit(floor_img, (floor_x1, floor_y))
    screen.blit(floor_img, (floor_x2, floor_y))
    
    # Draw the player image
    screen.blit(car_img, (player_x, player_y))

    # Draw the obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)

    pygame.display.flip()

pygame.quit()
