import pygame
import sys
import random
import time
from pygame import mixer
import tkinter as tk

pygame.init()

WIDTH, HEIGHT = 1272, 705
font_game_over = pygame.font.Font('GloriousChristmas-BLWWB.ttf', 100)
font_score = pygame.font.Font('GloriousChristmas-BLWWB.ttf', 36)

def game_over_menu(level):
    replay_button = Button('replay_button.png', (WIDTH//2 - 210, HEIGHT//2 + 100), 150, 150)
    main_menu_button = Button('menu_button.png', (WIDTH//2 + 20, HEIGHT//2 + 100), 150, 150)

    while True:
        screen.blit(map, (0, 0))
        draw_text('Game Over', font_game_over, WHITE, WIDTH // 2 - 15, HEIGHT // 2)

        # Draw Replay and Main Menu buttons
        replay_button.draw(screen)
        main_menu_button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button.is_clicked(mouse_pos):
                    return 'replay'
                elif main_menu_button.is_clicked(mouse_pos):
                    return 'main_menu'

def level1():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Dodge")

    pygame.init()
    mixer.music.load('level_1/key.mp3')
    mixer.music.play(-1)

    BG = pygame.transform.scale(pygame.image.load("level_1/key_bg.jpg"), (WIDTH, HEIGHT))

    PLAYER_WIDTH = 150
    PLAYER_HEIGHT = 120
    PLAYER_VEL = 5

    KEY_WIDTH = 50
    KEY_HEIGHT = 50
    KEY_VEL = 3

    SPECIAL_KEY_WIDTH = 100
    SPECIAL_KEY_HEIGHT = 100
    SPECIAL_KEY_VEL = 5


    def load_and_scale_image(image_path, width, height):
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))

    harry_right = load_and_scale_image("level_1/harry_right.png", PLAYER_WIDTH, PLAYER_HEIGHT)
    harry_left = load_and_scale_image("level_1/harry_left.png", PLAYER_WIDTH, PLAYER_HEIGHT)

    harry_mask_right = pygame.mask.from_surface(harry_right)
    harry_mask_left = pygame.mask.from_surface(harry_left)

    images = ["level_1/key1.png", "level_1/key2.png", "level_1/key3.png", "level_1/key4.png"]
    loaded_images = [load_and_scale_image(image, KEY_WIDTH, KEY_HEIGHT) for image in images]

    special_key_image = load_and_scale_image("level_1/collect.png", SPECIAL_KEY_WIDTH, SPECIAL_KEY_HEIGHT)

    def choose_random_image():
        return random.choice(loaded_images)

    def draw(player, elapsed_time, flies, special_flies, score):
        WIN.blit(BG, (0, 0))

        score_text = font_score.render(f"Score: {score}", 1, "white")

        WIN.blit(score_text, (20,20))

        if player.direction == 'right':
            WIN.blit(harry_right, (player.x, player.y))
        else:
            WIN.blit(harry_left, (player.x, player.y))

        for key in flies:
            WIN.blit(key.image, (key.x, key.y))

        for special_key in special_flies:
            WIN.blit(special_key.image, (special_key.x, special_key.y))

        pygame.display.update()

    def main():
        run = True

        class Player:
            def __init__(self):
                self.x = (WIDTH - PLAYER_WIDTH) // 2
                self.y = (HEIGHT - PLAYER_HEIGHT) // 2
                self.width = PLAYER_WIDTH
                self.height = PLAYER_HEIGHT
                self.direction = 'right'

        player = Player()

        clock = pygame.time.Clock()
        key_time = time.time()
        elapsed_time = 0

        key_add_increment = 1500
        key_count = 0

        class Key:
            def __init__(self, image, x, y):
                self.image = image
                self.x = x
                self.y = y
                self.is_special = False

        class SpecialKey(Key):
            def __init__(self, x, y):
                super().__init__(special_key_image, x, y)
                self.is_special = True

        flies = []
        special_flies = []
        score = 0

        while run:
            key_count += clock.tick(60)
            elapsed_time = time.time() - key_time

            if key_count > key_add_increment:
                for _ in range(5):
                    while True:
                        key_x = random.randint(0, WIDTH - KEY_WIDTH)
                        key_y = -KEY_HEIGHT
                        overlaps = False

                        for existing_key in flies + special_flies:
                            if (key_x < existing_key.x + KEY_WIDTH and
                                    key_x + KEY_WIDTH > existing_key.x and
                                    key_y < existing_key.y + KEY_HEIGHT and
                                    key_y + KEY_HEIGHT > existing_key.y):
                                overlaps = True
                                break

                        if not overlaps:
                            if random.random() < 0.03:  # 10% chance to spawn a special key
                                special_key = SpecialKey(key_x, key_y)
                                special_flies.append(special_key)
                            else:
                                key_image = choose_random_image()
                                key = Key(key_image, key_x, key_y)
                                flies.append(key)
                            break

                key_add_increment = max(200, key_add_increment - 10)
                key_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
                player.direction = 'left'
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
                player.direction = 'right'

            for special_key in special_flies[:]:
                special_key.y += SPECIAL_KEY_VEL
                special_key_rect = pygame.Rect(special_key.x, special_key.y, SPECIAL_KEY_WIDTH, SPECIAL_KEY_HEIGHT)
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                relative_position = (special_key_rect.x - player_rect.x, special_key_rect.y - player_rect.y)

                if player.direction == 'right':
                    if harry_mask_right.overlap(pygame.mask.from_surface(special_key.image), relative_position):
                        special_flies.remove(special_key)
                        score += 1
                else:
                    if harry_mask_left.overlap(pygame.mask.from_surface(special_key.image), relative_position):
                        special_flies.remove(special_key)
                        score += 1

            for key in flies[:]:
                key.y += KEY_VEL
                key_rect = pygame.Rect(key.x, key.y, KEY_WIDTH, KEY_HEIGHT)
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                relative_position = (key_rect.x - player_rect.x, key_rect.y - player_rect.y)

                if player.direction == 'right':
                    if harry_mask_right.overlap(pygame.mask.from_surface(key.image), relative_position):
                        mixer.music.stop()
                        action = game_over_menu(1)
                        if action == 'replay':
                            level1()
                        elif action == 'main_menu':
                            all()
                else:
                    if harry_mask_left.overlap(pygame.mask.from_surface(key.image), relative_position):
                        mixer.music.stop()
                        action = game_over_menu(1)
                        if action == 'replay':
                            level1()
                        elif action == 'main_menu':
                            all()
            draw(player, elapsed_time, flies, special_flies, score)

        

    if __name__ == "__main__":
        main()

def level2():
    pygame.init()
    mixer.music.load('level_2/spiders.mp3')
    mixer.music.play(-1)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car")
    BG = pygame.transform.scale(pygame.image.load("level_2/bg.jpg"), (WIDTH, HEIGHT))
    fps = 60
    white = [255, 255, 255]
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
                    mixer.music.stop()
                    action = game_over_menu(2)
                    if action == 'replay':
                        level2()
                    elif action == 'main_menu':
                        all()

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

        
def level3():
    mixer.music.load('level_3/hippogriff.mp3')
    mixer.music.play(-1)

    clock = pygame.time.Clock()
    fps = 60

    player_width = 150
    player_height = 132

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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


    #load images
    bg = pygame.image.load('level_3/bg.png')


    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                img = pygame.transform.scale(pygame.image.load(f'level_3/buckbeak{num}.png').convert_alpha(), (player_width, player_height))
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
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and not self.clicked:
                    self.clicked = True
                    self.vel = -10
                if not keys[pygame.K_SPACE]:
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
            self.image = pygame.image.load('level_3/tower.png')
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

    flappy = Bird(100, int(HEIGHT / 2))

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
                    mixer.music.stop()
                    action = game_over_menu(3)
                    if action == 'replay':
                        level3()    
                    elif action == 'main_menu':
                        main()
                elif pipe.rect.right < bird.rect.left and not pipe.score_counted:
                    score += 0.5
                    pipe.score_counted = True

        #check if bird has hit the ground
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False
            mixer.music.stop()
            action = game_over_menu(3)
            if action == 'replay':
                level3()
            elif action == 'main_menu':
                main()


        if game_over == False and flying == True:

            #generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
                top_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, 1)
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not flying and not game_over:
                flying = True

        score_text = font_score.render(f"Score: {score}", 1, "white")
        screen.blit(score_text, (20, 20))

        pygame.display.update()


# Set up the screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Load background image
background_image = pygame.transform.scale(pygame.image.load("back.jpg"), (WIDTH, HEIGHT))
map = pygame.transform.scale(pygame.image.load("fire.jpg"),(WIDTH, HEIGHT))
level_menu = pygame.transform.scale(pygame.image.load("level_menu.png"),(WIDTH, HEIGHT))

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Button class
class Button:
    def __init__(self, image, pos, img_width, img_height):
        self.image = pygame.transform.scale(pygame.image.load(image), (img_width, img_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Function for the main menu
def main_menu():
    play_button = Button('button2.png', (150, 470), 215, 145)

    while True:
        screen.blit(background_image, (0, 0))

        # Draw Play button
        play_button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.is_clicked(mouse_pos):
                    level = level_select()
                    if level:
                        return level

# Function for level selection menu
def level_select():
    level1_button = Button('level10.png', (WIDTH//2 - 540, HEIGHT//2 - 300), 215, 215)
    level2_button = Button('level20.png', (WIDTH//2 - 230, HEIGHT//2 - 180), 215, 215)
    level3_button = Button('level30.png', (WIDTH//2 + 100, HEIGHT//2 - 85), 215, 215)

    while True:
        screen.blit(level_menu, (0, 0))

        # Draw level buttons
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level1_button.is_clicked(mouse_pos):
                    return 1
                elif level2_button.is_clicked(mouse_pos):
                    return 2
                elif level3_button.is_clicked(mouse_pos):
                    return 3

# Main function
def main():
    selected_level = main_menu()
    if selected_level == 1:
        level1()
    elif selected_level == 2:
        level2()
    else:
        level3()

def all():
    main()

if __name__ == "__main__":
    main()
