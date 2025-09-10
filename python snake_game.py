import pygame
import random
import os

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Window
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game Pro")

# Fonts
font = pygame.font.SysFont("bahnschrift", 30)
big_font = pygame.font.SysFont("comicsansms", 50)

# Clock
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Leaderboard file
HIGHSCORE_FILE = "leaderboard.txt"


# ---------------------- Utility Functions ----------------------
def load_highscore():
    """Load High Score from file"""
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def save_highscore(score):
    """Save High Score to file"""
    high = load_highscore()
    if score > high:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))


def draw_text(text, color, size, x, y, center=True):
    """Draw text helper"""
    font_obj = pygame.font.SysFont("bahnschrift", size)
    msg = font_obj.render(text, True, color)
    rect = msg.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    WIN.blit(msg, rect)


# ---------------------- Snake Game Functions ----------------------
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(WIN, GREEN, [x[0], x[1], snake_block, snake_block])


def game_loop():
    game_over = False
    x = WIDTH // 2
    y = HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore(score)
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -snake_block, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = snake_block, 0
                elif event.key == pygame.K_UP and y_change == 0:
                    x_change, y_change = 0, -snake_block
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change, y_change = 0, snake_block

        # Wall collision
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            save_highscore(score)
            return "menu"

        # Move snake
        x += x_change
        y += y_change
        WIN.fill(BLUE)
        pygame.draw.rect(WIN, YELLOW, [foodx, foody, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                save_highscore(score)
                return "menu"

        our_snake(snake_block, snake_list)

        # Show score
        draw_text(f"Score: {score}", BLACK, 25, 5, 5, center=False)
        draw_text(f"High Score: {load_highscore()}", BLACK, 25, WIDTH-5, 5, center=False)

        pygame.display.update()

        # Food eaten
        if x == foodx and y == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 10

        clock.tick(snake_speed)


# ---------------------- Main Menu ----------------------
def main_menu():
    while True:
        WIN.fill(WHITE)
        draw_text("🐍 Snake Game Pro", RED, 50, WIDTH // 2, HEIGHT // 4)
        draw_text("1. Play", BLACK, 35, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("2. Quit", BLACK, 35, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text(f"🏆 High Score: {load_highscore()}", GREEN, 30, WIDTH // 2, HEIGHT - 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "quit"


# ---------------------- Game Runner ----------------------
def main():
    while True:
        menu_choice = main_menu()
        if menu_choice == "play":
            result = game_loop()
            if result == "quit":
                break
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()

