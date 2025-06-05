import pygame
import os
from settings import WIDTH, HEIGHT, CELL_SIZE, FPS, ASSET_PATH
from snake import Snake
from fruit import Fruit
import random
import ui
import time  # For timing level up message

def load_image(name, size=(CELL_SIZE, CELL_SIZE)):
    img = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
    return pygame.transform.scale(img, size)

def generate_obstacles(snake_body, fruit_pos, num=10):
    obs = []
    while len(obs) < num:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        pos = (x, y)
        # Avoid placing obstacles on snake or fruit or duplicates
        if pos not in snake_body and pos != fruit_pos and pos not in obs:
            obs.append(pos)
    return obs

def draw_obstacles(screen, obstacles):
    color = (139, 69, 19)  # Brown color
    for pos in obstacles:
        pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game Hybrid')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 25)

    # Load images
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
        "heart": load_image("heart.png", size=(80, 80)),
    }

    lives = 3
    score = 0
    high_score = 0
    game_state = "START"

    snake = Snake(images)
    fruit = Fruit(snake.get_body())
    direction = 'RIGHT'
    change_to = direction

    # Levels and speeds
    level = 1
    obstacles = []  # no obstacles in level 1

    LEVEL_SPEEDS = {
        1: 10,  # Normal speed
        2: 15,  # Faster speed
    }

    # Level up message control (time-based)
    show_level_up = False
    level_up_start_time = 0
    LEVEL_UP_DISPLAY_SECONDS = 3  # seconds

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            elif game_state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = "START"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return
            elif game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return

        if game_state == "START":
            clicked_button = ui.draw_start_menu(screen, WIDTH, HEIGHT)
            if clicked_button == "start":
                lives = 3
                score = 0
                snake.reset()
                change_to = 'RIGHT'
                direction = 'RIGHT'
                fruit = Fruit(snake.get_body())
                level = 1
                obstacles = []
                show_level_up = False
                game_state = "PLAYING"
            elif clicked_button == "info":
                game_state = "INFO"

        elif game_state == "INFO":
            result = ui.draw_info_screen(screen, WIDTH, HEIGHT)
            if result == "back":
                game_state = "START"

        elif game_state == "GAME_OVER":
            action = ui.draw_game_over_screen(screen, WIDTH, HEIGHT, score, high_score)
            if action == "restart":
                lives = 3
                score = 0
                snake.reset()
                change_to = 'RIGHT'
                direction = 'RIGHT'
                fruit = Fruit(snake.get_body())
                level = 1
                obstacles = []
                show_level_up = False
                game_state = "PLAYING"
            elif action == "quit":
                pygame.quit()
                return

        elif game_state == "YOU_WIN":
            action = ui.draw_you_win_screen(screen, WIDTH, HEIGHT, score, high_score)
            if action == "restart":
                lives = 3
                score = 0
                snake.reset()
                change_to = 'RIGHT'
                direction = 'RIGHT'
                fruit = Fruit(snake.get_body())
                level = 1
                obstacles = []
                show_level_up = False
                game_state = "PLAYING"
            elif action == "quit":
                pygame.quit()
                return

        elif game_state == "PLAYING":
            direction = change_to
            snake.move(direction)

            if snake.get_head_pos() == fruit.get_pos():
                score += 1
                if score > high_score:
                    high_score = score

                # Level up at score 10 from level 1 to 2
                if score >= 10 and level == 1:
                    level = 2
                    obstacles = generate_obstacles(snake.get_body(), fruit.get_pos(), num=10)
                    show_level_up = True
                    level_up_start_time = time.time()

                if score >= 30:
                    game_state = "YOU_WIN"
                else:
                    # Ensure fruit doesn't spawn on obstacles in level 2
                    if level == 2:
                        fruit.spawn(snake.get_body() + obstacles)
                    else:
                        fruit.spawn(snake.get_body())

            else:
                snake.shrink()

            head = snake.get_head_pos()
            hit_wall = (
                head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT
            )
            hit_self = head in snake.get_body()[1:]
            hit_obstacle = head in obstacles if level == 2 else False

            if hit_wall or hit_self or hit_obstacle:
                lives -= 1
                if score > high_score:
                    high_score = score
                if lives == 0:
                    game_state = "GAME_OVER"
                else:
                    snake.reset()
                    change_to = 'RIGHT'
                    direction = 'RIGHT'
                    fruit = Fruit(snake.get_body())
                    if level == 2:
                        obstacles = generate_obstacles(snake.get_body(), fruit.get_pos(), num=10)

            ui.draw_background(screen)

            # Draw obstacles only in level 2
            if level == 2:
                draw_obstacles(screen, obstacles)

            snake.draw(screen)
            screen.blit(
                images["fruit"],
                pygame.Rect(fruit.get_pos()[0], fruit.get_pos()[1], CELL_SIZE, CELL_SIZE)
            )

            # Show level up message at the top center for 3 seconds
            if show_level_up:
                elapsed = time.time() - level_up_start_time
                if elapsed < LEVEL_UP_DISPLAY_SECONDS:
                    message = "LEVEL 2 REACHED!"
                    level_up_font = pygame.font.SysFont('arial', 40, bold=True)
                    text_surf = level_up_font.render(message, True, (255, 215, 0))
                    text_rect = text_surf.get_rect(midtop=(WIDTH // 2, 10))  # 10 px from top center

                    # Draw background box behind text
                    padding_x, padding_y = 20, 10
                    bg_rect = pygame.Rect(
                        text_rect.left - padding_x,
                        text_rect.top - padding_y,
                        text_rect.width + padding_x * 2,
                        text_rect.height + padding_y * 2,
                    )
                    pygame.draw.rect(screen, (30, 30, 30), bg_rect, border_radius=10)
                    pygame.draw.rect(screen, (255, 215, 0), bg_rect, 3, border_radius=10)

                    screen.blit(text_surf, text_rect)
                else:
                    show_level_up = False

            ui.display_score(screen, font, score)
            ui.display_lives(screen, font, lives, images["heart"])

        pygame.display.update()
        clock.tick(LEVEL_SPEEDS[level])


if __name__ == '__main__':
    main()
