import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1272, 705
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("key_bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 150
PLAYER_HEIGHT = 120

PLAYER_VEL = 5
FLY_WIDTH = 50
FLY_HEIGHT = 50
FLY_VEL = 3

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


def choose_random_image():
    return random.choice(loaded_images)

def draw(player, elapsed_time, flies):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    if player.direction == 'right':  
        WIN.blit(harry_right, (player.x, player.y))
    else:
        WIN.blit(harry_left, (player.x, player.y))

    for fly in flies:
        WIN.blit(fly.image, (fly.x, fly.y))

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

    fly_add_increment = 2000
    fly_count = 0

    class Fly:
        def __init__(self, image, x, y):
            self.image = image
            self.x = x
            self.y = y

    flies = []
    hit = False

    while run:
        fly_count += clock.tick(60)
        elapsed_time = time.time() - flyt_time

        if fly_count > fly_add_increment:
            for _ in range(5):
                while True:
                    fly_x = random.randint(0, WIDTH - FLY_WIDTH)
                    fly_y = -FLY_HEIGHT
                    overlaps = False

                    for existing_fly in flies:
                        if (fly_x < existing_fly.x + FLY_WIDTH and
                            fly_x + FLY_WIDTH > existing_fly.x and
                            fly_y < existing_fly.y + FLY_HEIGHT and
                            fly_y + FLY_HEIGHT > existing_fly.y):
                            overlaps = True
                            break

                    if not overlaps:
                        fly_image = choose_random_image()
                        fly = Fly(fly_image, fly_x, fly_y)
                        flies.append(fly)
                        break

            fly_add_increment = max(200, fly_add_increment - 50)
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

        for fly in flies[:]:
            fly.y += FLY_VEL
            fly_rect = pygame.Rect(fly.x, fly.y, FLY_WIDTH, FLY_HEIGHT)
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            relative_position = (fly_rect.x - player_rect.x, fly_rect.y - player_rect.y)

            if player.direction == 'right':
                if harry_mask_right.overlap(pygame.mask.from_surface(fly.image), relative_position):
                    flies.remove(fly)
                    hit = True
                    break
            else:
                if harry_mask_left.overlap(pygame.mask.from_surface(fly.image), relative_position):
                    flies.remove(fly)
                    hit = True
                    break

        if hit:
            lost_text = FONT.render("Wrong key!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            break

        draw(player, elapsed_time, flies)

    pygame.quit()


if __name__ == "__main__":
    main()
