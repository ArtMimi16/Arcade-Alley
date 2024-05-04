import pygame
import time
import random
from pygame import mixer

pygame.font.init()

WIDTH, HEIGHT = 1272, 705
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

pygame.init()
mixer.music.load('key.mp3')
mixer.music.play(-1)

BG = pygame.transform.scale(pygame.image.load("key_bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 150
PLAYER_HEIGHT = 120
PLAYER_VEL = 5

FLY_WIDTH = 50
FLY_HEIGHT = 50
FLY_VEL = 3

SPECIAL_FLY_WIDTH = 100
SPECIAL_FLY_HEIGHT = 100
SPECIAL_FLY_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

def load_and_scale_image(image_path, width, height):
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

harry_right = load_and_scale_image("harry_right.png", PLAYER_WIDTH, PLAYER_HEIGHT)
harry_left = load_and_scale_image("harry_left.png", PLAYER_WIDTH, PLAYER_HEIGHT)

harry_mask_right = pygame.mask.from_surface(harry_right)
harry_mask_left = pygame.mask.from_surface(harry_left)

images = ["fly1.png", "fly2.png", "fly3.png", "fly4.png"]
loaded_images = [load_and_scale_image(image, FLY_WIDTH, FLY_HEIGHT) for image in images]

special_fly_image = load_and_scale_image("collect.png", SPECIAL_FLY_WIDTH, SPECIAL_FLY_HEIGHT)

def choose_random_image():
    return random.choice(loaded_images)

def draw(player, elapsed_time, flies, special_flies, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")

    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (10, 50))

    if player.direction == 'right':
        WIN.blit(harry_right, (player.x, player.y))
    else:
        WIN.blit(harry_left, (player.x, player.y))

    for fly in flies:
        WIN.blit(fly.image, (fly.x, fly.y))

    for special_fly in special_flies:
        WIN.blit(special_fly.image, (special_fly.x, special_fly.y))

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
    flyt_time = time.time()
    elapsed_time = 0

    fly_add_increment = 1500
    fly_count = 0

    class Fly:
        def __init__(self, image, x, y):
            self.image = image
            self.x = x
            self.y = y
            self.is_special = False

    class SpecialFly(Fly):
        def __init__(self, x, y):
            super().__init__(special_fly_image, x, y)
            self.is_special = True

    flies = []
    special_flies = []
    score = 0

    while run:
        fly_count += clock.tick(60)
        elapsed_time = time.time() - flyt_time

        if fly_count > fly_add_increment:
            for _ in range(5):
                while True:
                    fly_x = random.randint(0, WIDTH - FLY_WIDTH)
                    fly_y = -FLY_HEIGHT
                    overlaps = False

                    for existing_fly in flies + special_flies:
                        if (fly_x < existing_fly.x + FLY_WIDTH and
                                fly_x + FLY_WIDTH > existing_fly.x and
                                fly_y < existing_fly.y + FLY_HEIGHT and
                                fly_y + FLY_HEIGHT > existing_fly.y):
                            overlaps = True
                            break

                    if not overlaps:
                        if random.random() < 0.03:  # 10% chance to spawn a special fly
                            special_fly = SpecialFly(fly_x, fly_y)
                            special_flies.append(special_fly)
                        else:
                            fly_image = choose_random_image()
                            fly = Fly(fly_image, fly_x, fly_y)
                            flies.append(fly)
                        break

            fly_add_increment = max(200, fly_add_increment - 10)
            fly_count = 0

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

        for special_fly in special_flies[:]:
            special_fly.y += SPECIAL_FLY_VEL
            special_fly_rect = pygame.Rect(special_fly.x, special_fly.y, SPECIAL_FLY_WIDTH, SPECIAL_FLY_HEIGHT)
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            relative_position = (special_fly_rect.x - player_rect.x, special_fly_rect.y - player_rect.y)

            if player.direction == 'right':
                if harry_mask_right.overlap(pygame.mask.from_surface(special_fly.image), relative_position):
                    special_flies.remove(special_fly)
                    score += 1
            else:
                if harry_mask_left.overlap(pygame.mask.from_surface(special_fly.image), relative_position):
                    special_flies.remove(special_fly)
                    score += 1

        for fly in flies[:]:
            fly.y += FLY_VEL
            fly_rect = pygame.Rect(fly.x, fly.y, FLY_WIDTH, FLY_HEIGHT)
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            relative_position = (fly_rect.x - player_rect.x, fly_rect.y - player_rect.y)

            if player.direction == 'right':
                if harry_mask_right.overlap(pygame.mask.from_surface(fly.image), relative_position):
                    run = False  # End game if regular fly is collected
            else:
                if harry_mask_left.overlap(pygame.mask.from_surface(fly.image), relative_position):
                    run = False  # End game if regular fly is collected

        draw(player, elapsed_time, flies, special_flies, score)

    pygame.quit()

if __name__ == "__main__":
    main()
