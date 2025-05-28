import pygame
import random
import os

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
CELL_NUMBER_X = WIDTH // CELL_SIZE
CELL_NUMBER_Y = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (220, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game Hybrid')
clock = pygame.time.Clock()
FPS = 10
font = pygame.font.SysFont('arial', 25)

ASSET_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets')

def load_image(name):
    img = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
    return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))

images = {
    "head_up": load_image("head_up.png"),
    "head_down": load_image("head_down.png"),
    "head_left": load_image("head_left.png"),
    "head_right": load_image("head_right.png"),
    "body_horizontal": load_image("body_horizontal.png"),
    "body_vertical": load_image("body_vertical.png"),
    "body_topleft": load_image("body_topleft.png"),
    "body_topright": load_image("body_topright.png"),
    "body_bottomleft": load_image("body_bottomleft.png"),
    "body_bottomright": load_image("body_bottomright.png"),
    "tail_up": load_image("tail_up.png"),
    "tail_down": load_image("tail_down.png"),
    "tail_left": load_image("tail_left.png"),
    "tail_right": load_image("tail_right.png"),
    "fruit": load_image("apple.png"),
}

def draw_background():
    light_green = (170, 215, 81)
    dark_green = (162, 209, 73)
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WIDTH, CELL_SIZE):
            color = light_green if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0 else dark_green
            pygame.draw.rect(screen, color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

def vector_from_coords(p1, p2):
    # Returns a tuple (dx, dy) as a difference between two points
    return (p2[0] - p1[0], p2[1] - p1[1])

def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        x, y = segment
        pos = (x, y)
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        if i == 0:  # Head
            head_dir = (snake_body[1][0] - segment[0], snake_body[1][1] - segment[1])
            if head_dir == (CELL_SIZE, 0):
                screen.blit(images["head_left"], rect)
            elif head_dir == (-CELL_SIZE, 0):
                screen.blit(images["head_right"], rect)
            elif head_dir == (0, CELL_SIZE):
                screen.blit(images["head_up"], rect)
            elif head_dir == (0, -CELL_SIZE):
                screen.blit(images["head_down"], rect)
        elif i == len(snake_body) - 1:  # Tail
            tail_dir = (snake_body[-2][0] - segment[0], snake_body[-2][1] - segment[1])
            if tail_dir == (CELL_SIZE, 0):
                screen.blit(images["tail_left"], rect)
            elif tail_dir == (-CELL_SIZE, 0):
                screen.blit(images["tail_right"], rect)
            elif tail_dir == (0, CELL_SIZE):
                screen.blit(images["tail_up"], rect)
            elif tail_dir == (0, -CELL_SIZE):
                screen.blit(images["tail_down"], rect)
        else:
            prev = snake_body[i + 1]
            next = snake_body[i - 1]
            prev_dir = (prev[0] - segment[0], prev[1] - segment[1])
            next_dir = (next[0] - segment[0], next[1] - segment[1])
            # Straight
            if prev_dir[0] == next_dir[0]:
                screen.blit(images["body_vertical"], rect)
            elif prev_dir[1] == next_dir[1]:
                screen.blit(images["body_horizontal"], rect)
            else:
                # Corners
                if (prev_dir == (0, -CELL_SIZE) and next_dir == (-CELL_SIZE, 0)) or (next_dir == (0, -CELL_SIZE) and prev_dir == (-CELL_SIZE, 0)):
                    screen.blit(images["body_topleft"], rect)
                elif (prev_dir == (0, -CELL_SIZE) and next_dir == (CELL_SIZE, 0)) or (next_dir == (0, -CELL_SIZE) and prev_dir == (CELL_SIZE, 0)):
                    screen.blit(images["body_topright"], rect)
                elif (prev_dir == (0, CELL_SIZE) and next_dir == (-CELL_SIZE, 0)) or (next_dir == (0, CELL_SIZE) and prev_dir == (-CELL_SIZE, 0)):
                    screen.blit(images["body_bottomleft"], rect)
                elif (prev_dir == (0, CELL_SIZE) and next_dir == (CELL_SIZE, 0)) or (next_dir == (0, CELL_SIZE) and prev_dir == (CELL_SIZE, 0)):
                    screen.blit(images["body_bottomright"], rect)

def draw_fruit(pos):
    screen.blit(images["fruit"], pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def display_score(score):
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def display_lives(lives):
    text = font.render(f'Lives: {lives}', True, YELLOW)
    screen.blit(text, (WIDTH - 120, 10))

def game_over_screen(score):
    screen.fill((0,0,0))
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//3 + 80))
    pygame.display.update()

def spawn_fruit(snake_body):
    while True:
        pos = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
        if pos not in snake_body:
            return pos

def reset_snake():
    pos = [WIDTH//2, HEIGHT//2]
    body = [pos[:], [pos[0]-CELL_SIZE, pos[1]], [pos[0]-2*CELL_SIZE, pos[1]]]
    direction = 'RIGHT'
    return pos, body, direction

def main():
    lives = 3
    score = 0

    snake_pos, snake_body, direction = reset_snake()
    change_to = direction
    fruit_pos = spawn_fruit(snake_body)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'
                else:
                    if event.key == pygame.K_r:
                        lives = 3
                        score = 0
                        snake_pos, snake_body, direction = reset_snake()
                        change_to = direction
                        fruit_pos = spawn_fruit(snake_body)
                        game_over = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return

        if not game_over:
            direction = change_to
            if direction == 'UP':
                snake_pos[1] -= CELL_SIZE
            elif direction == 'DOWN':
                snake_pos[1] += CELL_SIZE
            elif direction == 'LEFT':
                snake_pos[0] -= CELL_SIZE
            elif direction == 'RIGHT':
                snake_pos[0] += CELL_SIZE

            snake_body.insert(0, list(snake_pos))
            if snake_pos == fruit_pos:
                score += 1
                fruit_pos = spawn_fruit(snake_body)
            else:
                snake_body.pop()

            hit_wall = (
                snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
                snake_pos[1] < 0 or snake_pos[1] >= HEIGHT
            )
            hit_self = snake_pos in snake_body[1:]

            if hit_wall or hit_self:
                lives -= 1
                if lives == 0:
                    game_over = True
                else:
                    snake_pos, snake_body, direction = reset_snake()
                    change_to = direction
                    fruit_pos = spawn_fruit(snake_body)

            draw_background()
            draw_snake(snake_body)
            draw_fruit(fruit_pos)
            display_score(score)
            display_lives(lives)
            pygame.display.update()
            clock.tick(FPS)
        else:
            game_over_screen(score)

if __name__ == '__main__':
    main()