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

def display_lives(screen, font, lives, heart_image):
    screen_width = screen.get_width()
    margin = 10

    lives_text = font.render(str(lives), True, (255, 255, 255))
    text_rect = lives_text.get_rect()

    heart_rect = heart_image.get_rect()
    heart_rect.topright = (screen_width - text_rect.width - margin - 10, margin)

    text_rect.midleft = (heart_rect.right + 10, heart_rect.centery)

    screen.blit(heart_image, heart_rect)
    screen.blit(lives_text, text_rect)

def draw_start_menu(screen, width, height):
    screen.fill((140, 198, 62))

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Fonts
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    subtitle_font = pygame.font.SysFont("Arial", 18)
    body_font = pygame.font.SysFont("Courier New", 14)
    button_font = pygame.font.SysFont("Arial", 16, bold=True)

    # Title
    title_text = title_font.render("SNAKE", True, (0, 70, 20))
    subtitle_text = subtitle_font.render("Eating Fruit Game", True, (30, 120, 40))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 30))
    screen.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, 75))

    # Description box
    pygame.draw.rect(screen, (172, 224, 144), (width // 2 - 180, 100, 360, 55), border_radius=8)
    pygame.draw.rect(screen, (30, 120, 40), (width // 2 - 180, 100, 360, 55), 2, border_radius=8)

    desc1 = body_font.render("Control your snake to eat fruits and grow!", True, (30, 70, 30))
    desc2 = body_font.render("Avoid walls and your own tail to survive.", True, (30, 70, 30))
    screen.blit(desc1, (width // 2 - desc1.get_width() // 2, 110))
    screen.blit(desc2, (width // 2 - desc2.get_width() // 2, 130))

    # Controls box
    pygame.draw.rect(screen, (192, 240, 172), (width // 2 - 160, 165, 320, 40), border_radius=8)
    control_text = body_font.render("Use", True, (30, 70, 30))
    screen.blit(control_text, (width // 2 - 130, 175))

    keys = ["↑", "↓", "←", "→"]
    for i, key in enumerate(keys):
        key_surf = body_font.render(key, True, (0, 50, 0))
        rect_x = width // 2 - 80 + i * 40
        pygame.draw.rect(screen, (144, 216, 144), (rect_x, 170, 30, 25), border_radius=4)
        pygame.draw.rect(screen, (30, 120, 40), (rect_x, 170, 30, 25), 2, border_radius=4)
        screen.blit(key_surf, (rect_x + 9, 173))

    move_text = body_font.render("  to move", True, (30, 70, 30))
    screen.blit(move_text, (width // 2 + 70, 175))

    # --- START BUTTON ---
    start_rect = pygame.Rect(width // 2 - 60, 230, 120, 35)
    start_hover = start_rect.collidepoint(mouse_pos)
    start_color = (46, 158, 77) if start_hover else (36, 138, 67)

    pygame.draw.rect(screen, start_color, start_rect, border_radius=6)
    pygame.draw.rect(screen, (0, 90, 40), start_rect, 2, border_radius=6)
    start_text = button_font.render("START GAME", True, (255, 255, 255))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, 238))

    # --- INFO BUTTON ---
    info_rect = pygame.Rect(width // 2 - 45, 280, 90, 30)
    info_hover = info_rect.collidepoint(mouse_pos)
    info_color = (255, 190, 40) if info_hover else (255, 170, 0)

    pygame.draw.rect(screen, info_color, info_rect, border_radius=5)
    pygame.draw.rect(screen, (255, 110, 0), info_rect, 2, border_radius=5)
    info_text = button_font.render("INFO", True, (0, 0, 0))
    screen.blit(info_text, (width // 2 - info_text.get_width() // 2, 287))

    pygame.display.update()

    # --- Handle Clicks ---
    if mouse_click[0]:  # Left click
        if start_hover:
            return "start"
        elif info_hover:
            return "info"

    return "menu"


def draw_game_over_screen(screen, width, height, score, high_score):
    screen.fill((140, 198, 62))  # Same background green as start menu

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Fonts (matching start menu fonts)
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    subtitle_font = pygame.font.SysFont("Arial", 18)
    body_font = pygame.font.SysFont("Courier New", 14)
    button_font = pygame.font.SysFont("Arial", 16, bold=True)

    # Title
    game_over_text = title_font.render("GAME OVER!", True, (0, 70, 20))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, 40))

    # Score box
    pygame.draw.rect(screen, (172, 224, 144), (width // 2 - 180, 100, 360, 80), border_radius=8)
    pygame.draw.rect(screen, (30, 120, 40), (width // 2 - 180, 100, 360, 80), 2, border_radius=8)

    final_score_text = body_font.render(f"Final Score: {score}", True, (30, 70, 30))
    high_score_text = body_font.render(f"High Score: {high_score}", True, (30, 70, 30))
    screen.blit(final_score_text, (width // 2 - final_score_text.get_width() // 2, 120))
    screen.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, 150))

    # Restart Button
    restart_rect = pygame.Rect(width // 2 - 140, 200, 120, 35)
    restart_hover = restart_rect.collidepoint(mouse_pos)
    restart_color = (46, 158, 77) if restart_hover else (36, 138, 67)
    pygame.draw.rect(screen, restart_color, restart_rect, border_radius=6)
    pygame.draw.rect(screen, (0, 90, 40), restart_rect, 2, border_radius=6)
    restart_text = button_font.render("RESTART", True, (255, 255, 255))
    screen.blit(restart_text, (restart_rect.x + (restart_rect.width - restart_text.get_width()) // 2,
                               restart_rect.y + 7))

    # Quit Button
    quit_rect = pygame.Rect(width // 2 + 20, 200, 120, 35)
    quit_hover = quit_rect.collidepoint(mouse_pos)
    quit_color = (255, 190, 40) if quit_hover else (255, 170, 0)
    pygame.draw.rect(screen, quit_color, quit_rect, border_radius=6)
    pygame.draw.rect(screen, (255, 110, 0), quit_rect, 2, border_radius=6)
    quit_text = button_font.render("QUIT", True, (0, 0, 0))
    screen.blit(quit_text, (quit_rect.x + (quit_rect.width - quit_text.get_width()) // 2,
                            quit_rect.y + 7))

    pygame.display.update()

    # Return values based on clicks
    if mouse_click[0]:  # Left click
        if restart_hover:
            return "restart"
        elif quit_hover:
            return "quit"
    return "game_over"