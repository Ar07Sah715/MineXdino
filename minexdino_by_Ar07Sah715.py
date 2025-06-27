
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 450
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -12
GROUND_HEIGHT = 40
BLOCK_SIZE = 30

WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 197, 94)
DIRT_BROWN = (139, 69, 19)
BLUE = (59, 130, 246)
DRAGON_COLOR = (31, 41, 55)
CACTUS_COLOR = (30, 132, 73)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("minexdino by Ar07.Sah715")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Player setup
player = pygame.Rect(80, HEIGHT - GROUND_HEIGHT - 30, 30, 30)
player_vel_y = 0
on_ground = True

# Game state
obstacles = []
score = 0
scroll_speed = 5
max_scroll_speed = 10
speed_increase_interval = 200
game_running = True
spawn_timer = 0
spawn_interval = random.randint(60, 180)

def draw_background():
    for y in range(0, HEIGHT, BLOCK_SIZE):
        for x in range(0, WIDTH, BLOCK_SIZE):
            if y < HEIGHT * 0.6:
                color = SKY_BLUE
            elif y < HEIGHT - GROUND_HEIGHT:
                color = DIRT_BROWN
            else:
                color = GRASS_GREEN
            pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))

def draw_player():
    pygame.draw.rect(screen, BLUE, player)
    eye = pygame.Rect(player.x + player.width // 3, player.y + player.height // 3, 5, 5)
    pygame.draw.rect(screen, (0, 0, 0), eye)

def draw_obstacles():
    for obs in obstacles:
        if obs['type'] == 'cactus':
            pygame.draw.rect(screen, CACTUS_COLOR, obs['rect'])
        else:
            r = obs['rect']
            pygame.draw.rect(screen, DRAGON_COLOR, (r.x, r.y + BLOCK_SIZE, r.width, BLOCK_SIZE))
            pygame.draw.rect(screen, DRAGON_COLOR, (r.x + r.width - 20, r.y + BLOCK_SIZE//2, 30, 10))
            pygame.draw.rect(screen, DRAGON_COLOR, (r.x + 15, r.y, 40, 10))
            pygame.draw.rect(screen, DRAGON_COLOR, (r.x, r.y + int(BLOCK_SIZE * 1.2), 10, 10))

def generate_obstacle():
    if random.random() < 0.3:
        height = BLOCK_SIZE * 2
        y = HEIGHT - GROUND_HEIGHT - 90 - random.randint(0, 50)
        rect = pygame.Rect(WIDTH, y, BLOCK_SIZE * 3, height)
        return {'rect': rect, 'type': 'dragon'}
    else:
        width = BLOCK_SIZE * random.randint(1, 2)
        height = BLOCK_SIZE * random.randint(2, 3)
        y = HEIGHT - GROUND_HEIGHT - height
        rect = pygame.Rect(WIDTH, y, width, height)
        return {'rect': rect, 'type': 'cactus'}

def reset_game():
    global obstacles, score, scroll_speed, game_running, spawn_timer, spawn_interval, player, player_vel_y
    player.y = HEIGHT - GROUND_HEIGHT - player.height
    player_vel_y = 0
    obstacles = []
    score = 0
    scroll_speed = 5
    spawn_timer = 0
    spawn_interval = random.randint(60, 180)
    game_running = True

# Main loop
while True:
    clock.tick(FPS)
    screen.fill(WHITE)
    draw_background()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_running and event.type == pygame.KEYDOWN:
            reset_game()

    if game_running:
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and on_ground:
            player_vel_y = JUMP_STRENGTH
            on_ground = False

        player_vel_y += GRAVITY
        player.y += player_vel_y

        if player.y + player.height >= HEIGHT - GROUND_HEIGHT:
            player.y = HEIGHT - GROUND_HEIGHT - player.height
            player_vel_y = 0
            on_ground = True

        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            obstacles.append(generate_obstacle())
            spawn_timer = 0
            spawn_interval = random.randint(60, 180)

        for obs in obstacles[:]:
            obs['rect'].x -= scroll_speed
            if player.colliderect(obs['rect']):
                game_running = False
            if obs['rect'].x + obs['rect'].width < 0:
                obstacles.remove(obs)
                score += 1
                if score % speed_increase_interval == 0 and scroll_speed < max_scroll_speed:
                    scroll_speed += 1

    draw_player()
    draw_obstacles()

    score_text = font.render(f"Score: {score}", True, (55, 55, 55))
    screen.blit(score_text, (20, 20))

    if not game_running:
        go_text = font.render("Game Over! Press any key to restart", True, (0, 0, 0))
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 20))
        final_score = font.render(f"Final Score: {score}", True, (0, 0, 0))
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 + 20))

    copyright_text = font.render("© copyright to Ar07Sah715", True, (100, 100, 100))
    screen.blit(copyright_text, (WIDTH - copyright_text.get_width() - 10, HEIGHT - 30))

    pygame.display.flip()
