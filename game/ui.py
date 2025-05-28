import pygame
from settings import WIDTH, HEIGHT, CELL_SIZE, WHITE, YELLOW, RED

def draw_background(screen):
    light_green = (170, 215, 81)
    dark_green = (162, 209, 73)
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WIDTH, CELL_SIZE):
            color = light_green if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0 else dark_green
            pygame.draw.rect(screen, color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

def display_score(screen, font, score):
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def display_lives(screen, font, lives):
    text = font.render(f'Lives: {lives}', True, YELLOW)
    screen.blit(text, (WIDTH - 120, 10))

def draw_start_menu(screen, font):
    screen.fill((50, 90, 40))
    title = font.render("SNAKE GAME", True, (255, 255, 255))
    instruct = font.render("Press SPACE to start", True, (255, 255, 0))
    controls = font.render("Arrows: Move   Q: Quit", True, (200, 200, 200))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(instruct, (WIDTH//2 - instruct.get_width()//2, HEIGHT//2))
    screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()

def draw_game_over_screen(screen, font, score, high_score):
    screen.fill((40, 40, 40))
    game_over_text = font.render("Game Over!", True, (220, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 200, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 50))
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//3 + 90))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//3 + 150))
    pygame.display.update()