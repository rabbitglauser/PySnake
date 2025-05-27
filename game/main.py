import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game with Lives')

clock = pygame.time.Clock()
FPS = 10

font = pygame.font.SysFont('arial', 25)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_snake(snake_body):
    for segment in snake_body:
        rect = pygame.Rect(segment[0] + 1, segment[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(screen, GREEN, rect)
        pygame.draw.rect(screen, DARK_GREEN, rect, 2)

def draw_fruit(pos):
    rect = pygame.Rect(pos[0] + 4, pos[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8)
    pygame.draw.rect(screen, RED, rect)

def display_score(score):
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def display_lives(lives):
    text = font.render(f'Lives: {lives}', True, YELLOW)
    screen.blit(text, (WIDTH - 120, 10))

def game_over_screen(score):
    screen.fill(BLACK)
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
                    # On game over screen
                    if event.key == pygame.K_r:
                        # Restart game
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

            hit_wall = (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
                        snake_pos[1] < 0 or snake_pos[1] >= HEIGHT)
            hit_self = snake_pos in snake_body[1:]

            if hit_wall or hit_self:
                lives -= 1
                if lives == 0:
                    game_over = True
                else:
                    snake_pos, snake_body, direction = reset_snake()
                    change_to = direction
                    fruit_pos = spawn_fruit(snake_body)

            screen.fill(BLACK)
            draw_grid()
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
