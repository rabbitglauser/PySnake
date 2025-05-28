import pygame
import os
from settings import WIDTH, HEIGHT, CELL_SIZE, FPS, ASSET_PATH
from snake import Snake
from fruit import Fruit
import ui

def load_image(name):
    img = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
    return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))

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
    }

    lives = 3
    score = 0
    high_score = 0
    game_state = "START"  # "START", "PLAYING", "GAME_OVER"

    snake = Snake(images)
    fruit = Fruit(snake.get_body())
    direction = 'RIGHT'
    change_to = direction

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if game_state == "START":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    lives = 3
                    score = 0
                    snake.reset()
                    change_to = 'RIGHT'
                    direction = 'RIGHT'
                    fruit = Fruit(snake.get_body())
                    game_state = "PLAYING"
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
            ui.draw_start_menu(screen, font)
        elif game_state == "GAME_OVER":
            ui.draw_game_over_screen(screen, font, score, high_score)
        elif game_state == "PLAYING":
            direction = change_to
            snake.move(direction)
            # Check fruit collision
            if snake.get_head_pos() == fruit.get_pos():
                score += 1
                fruit.spawn(snake.get_body())
            else:
                snake.shrink()

            # Check collisions
            head = snake.get_head_pos()
            hit_wall = (
                head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT
            )
            hit_self = head in snake.get_body()[1:]

            if hit_wall or hit_self:
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

            ui.draw_background(screen)
            snake.draw(screen)
            screen.blit(images["fruit"], pygame.Rect(fruit.get_pos()[0], fruit.get_pos()[1], CELL_SIZE, CELL_SIZE))
            ui.display_score(screen, font, score)
            ui.display_lives(screen, font, lives)
            pygame.display.update()
            clock.tick(FPS)

if __name__ == '__main__':
    main()