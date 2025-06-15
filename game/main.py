import os
from settings import WIDTH, HEIGHT, CELL_SIZE, FPS, ASSET_PATH
from snake import Snake
from fruit import Fruit
import random
import ui
import time
import math  # For bobbing effect

def load_image(name, size=(CELL_SIZE, CELL_SIZE)):
    import pygame
    img = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
    return pygame.transform.scale(img, size)

def generate_obstacles(snake_body, fruit_pos, level):
    num = random.choice([3, 4]) if level >= 2 else 0
    obs = []
    while len(obs) < num:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        pos = (x, y)
        if pos not in snake_body and pos != fruit_pos and pos not in obs:
            obs.append(pos)
    return obs

def draw_obstacles(screen, obstacles, wall_img):
    import pygame
    for pos in obstacles:
        screen.blit(wall_img, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

class Enemy:
    def __init__(self, enemy_img):
        self.img = enemy_img
        self.size = enemy_img.get_width()
        self.reset()

    def reset(self):
        import random
        self.direction = random.choice(['left', 'right'])
        self.y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if self.direction == 'right':
            self.x = -CELL_SIZE
            self.speed = CELL_SIZE // 2
        else:
            self.x = WIDTH
            self.speed = -CELL_SIZE // 2

    def update(self):
        self.x += self.speed
        if self.direction == 'right' and self.x > WIDTH:
            self.reset()
        elif self.direction == 'left' and self.x < -CELL_SIZE:
            self.reset()

    def draw(self, screen):
        import pygame
        screen.blit(self.img, pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))

    def collides_with_snake(self, snake_body):
        for (sx, sy) in snake_body:
            if (self.x < sx + CELL_SIZE and self.x + CELL_SIZE > sx and
                self.y < sy + CELL_SIZE and self.y + CELL_SIZE > sy):
                return True
        return False

# --- Coin class with floating & bobbing effect ---
class Coin:
    def __init__(self, coin_img, snake_body, fruit_pos, obstacles):
        self.img = coin_img
        self.spawn(snake_body, fruit_pos, obstacles)
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.move_counter = 0
        self.base_y = self.y  # For bobbing
        self.bob_phase = random.uniform(0, 2 * math.pi)  # Start at a random phase

    def spawn(self, snake_body, fruit_pos, obstacles):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            pos = (x, y)
            occupied = snake_body + [fruit_pos]
            if obstacles:
                occupied += obstacles
            if pos not in occupied:
                self.x, self.y = pos
                self.base_y = self.y
                self.bob_phase = random.uniform(0, 2 * math.pi)
                break

    def update(self, snake_body, fruit_pos, obstacles):
        # Move every few frames for a less jittery look
        self.move_counter += 1
        if self.move_counter % 8 == 0:
            dx, dy = 0, 0
            if self.direction == 'UP':
                dy = -CELL_SIZE
            elif self.direction == 'DOWN':
                dy = CELL_SIZE
            elif self.direction == 'LEFT':
                dx = -CELL_SIZE
            elif self.direction == 'RIGHT':
                dx = CELL_SIZE
            new_x = self.x + dx
            new_y = self.base_y + dy  # base_y tracks grid movement
            blocked = False
            if (new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT):
                blocked = True
            else:
                new_pos = (new_x, new_y)
                occupied = snake_body + [fruit_pos]
                if obstacles:
                    occupied += obstacles
                if new_pos in occupied:
                    blocked = True
            if blocked:
                dirs = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                dirs.remove(self.direction)
                self.direction = random.choice(dirs)
            else:
                self.x = new_x
                self.base_y = new_y  # update grid "anchor" position for bobbing

    def draw(self, screen):
        import pygame
        # Floating bobbing animation
        # Bob amplitude and speed
        amplitude = 6  # pixels
        speed = 2.4    # radians/sec
        # Use pygame.time.get_ticks() for smooth animation
        ticks = pygame.time.get_ticks() / 1000.0  # seconds
        bob_offset = amplitude * math.sin(speed * ticks + self.bob_phase)
        rect = pygame.Rect(self.x, self.base_y + bob_offset, CELL_SIZE, CELL_SIZE)
        screen.blit(self.img, rect)

    def get_pos(self):
        # For collision, use grid position (anchor)
        return (self.x, self.base_y)

def main():
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game Hybrid')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 25)

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
        "wall": load_image("wall.png"),
        "enemy": load_image("enemy.png"),
        "coin": load_image("coin.png"),
    }

    score = 0
    high_score = 0
    coin_score = 0
    game_state = "START"

    snake = Snake(images)
    fruit = Fruit(snake.get_body())
    direction = 'RIGHT'
    change_to = direction

    level = 1
    obstacles = []
    enemy = None

    LEVEL_SPEEDS = {
        1: 10,
        2: 14,
        3: 17,
    }

    show_level_up = False
    level_up_start_time = 0
    LEVEL_UP_DISPLAY_SECONDS = 2.3

    coin = Coin(images["coin"], snake.get_body(), fruit.get_pos(), obstacles)

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
                score = 0
                coin_score = 0
                snake.reset()
                change_to = 'RIGHT'
                direction = 'RIGHT'
                fruit = Fruit(snake.get_body())
                level = 1
                obstacles = []
                enemy = None
                show_level_up = False
                coin = Coin(images["coin"], snake.get_body(), fruit.get_pos(), obstacles)
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
                score = 0
                coin_score = 0
                snake.reset()
                change_to = 'RIGHT'
                direction = 'RIGHT'
                fruit = Fruit(snake.get_body())
                level = 1
                obstacles = []
                enemy = None
                show_level_up = False
                coin = Coin(images["coin"], snake.get_body(), fruit.get_pos(), obstacles)
                game_state = "PLAYING"
            elif action == "quit":
                pygame.quit()
                return

        elif game_state == "YOU_WIN":
            action = ui.draw_you_win_screen(screen, WIDTH, HEIGHT, score, high_score)
            if action == "restart":
                score = 0
                coin_score = 0
                snake.reset()
                change_to = 'RIGHT'
                direction = 'RIGHT'
                fruit = Fruit(snake.get_body())
                level = 1
                obstacles = []
                enemy = None
                show_level_up = False
                coin = Coin(images["coin"], snake.get_body(), fruit.get_pos(), obstacles)
                game_state = "PLAYING"
            elif action == "quit":
                pygame.quit()
                return

        elif game_state == "PLAYING":
            direction = change_to
            snake.move(direction)

            coin.update(snake.get_body(), fruit.get_pos(), obstacles)

            if snake.get_head_pos() == coin.get_pos():
                coin_score += 1
                coin.spawn(snake.get_body(), fruit.get_pos(), obstacles)

            if snake.get_head_pos() == fruit.get_pos():
                score += 1
                if score > high_score:
                    high_score = score

                if score >= 10 and level == 1:
                    level = 2
                    obstacles = generate_obstacles(snake.get_body(), fruit.get_pos(), level)
                    show_level_up = True
                    level_up_start_time = time.time()
                    coin.spawn(snake.get_body(), fruit.get_pos(), obstacles)

                if score >= 15 and level == 2:
                    level = 3
                    obstacles = generate_obstacles(snake.get_body(), fruit.get_pos(), level)
                    enemy = Enemy(images["enemy"])
                    show_level_up = True
                    level_up_start_time = time.time()
                    coin.spawn(snake.get_body(), fruit.get_pos(), obstacles)

                if score >= 30:
                    game_state = "YOU_WIN"
                else:
                    if level >= 2:
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
            hit_obstacle = head in obstacles if level >= 2 else False

            hit_enemy = False
            if level == 3 and enemy is not None:
                enemy.update()
                hit_enemy = enemy.collides_with_snake(snake.get_body())

            if hit_wall or hit_self or hit_obstacle or hit_enemy:
                game_state = "GAME_OVER"

            ui.draw_background(screen)

            if level >= 2:
                draw_obstacles(screen, obstacles, images["wall"])

            snake.draw(screen)
            coin.draw(screen)
            screen.blit(
                images["fruit"],
                pygame.Rect(fruit.get_pos()[0], fruit.get_pos()[1], CELL_SIZE, CELL_SIZE)
            )

            if level == 3 and enemy is not None:
                enemy.draw(screen)

            if level >= 2:
                small_font = pygame.font.SysFont('arial', 18)
                score_surf = small_font.render(f"Score: {score}", True, (255,255,255))
                coin_surf = small_font.render(f"Coins: {coin_score}", True, (255,223,0))
                score_bg = pygame.Surface((max(score_surf.get_width(), coin_surf.get_width())+12, score_surf.get_height()*2+9), pygame.SRCALPHA)
                score_bg.fill((0,0,0,100))
                screen.blit(score_bg, (10,10))
                screen.blit(score_surf, (16,13))
                screen.blit(coin_surf, (16,13+score_surf.get_height()+2))
                lvl_surf = small_font.render(f"Level: {level}", True, (255,255,120))
                lvl_bg = pygame.Surface((lvl_surf.get_width()+14, lvl_surf.get_height()+6), pygame.SRCALPHA)
                lvl_bg.fill((0,0,0,90))
                screen.blit(lvl_bg, (WIDTH-lvl_surf.get_width()-24, 10))
                screen.blit(lvl_surf, (WIDTH-lvl_surf.get_width()-17, 13))
            else:
                ui.display_score(screen, font, score)
                small_font = pygame.font.SysFont('arial', 18)
                coin_surf = small_font.render(f"Coins: {coin_score}", True, (255,223,0))
                screen.blit(coin_surf, (12, 40))

            if show_level_up:
                elapsed = time.time() - level_up_start_time
                if elapsed < LEVEL_UP_DISPLAY_SECONDS:
                    if level == 2:
                        message = "LEVEL 2 REACHED!"
                    elif level == 3:
                        message = "LEVEL 3 REACHED!"
                    else:
                        message = f"LEVEL {level} REACHED!"
                    level_up_font = pygame.font.SysFont('arial', 28, bold=True)
                    text_surf = level_up_font.render(message, True, (255, 215, 0))
                    text_rect = text_surf.get_rect(midtop=(WIDTH // 2, 16))
                    bg_rect = pygame.Rect(
                        text_rect.left - 10, text_rect.top - 5,
                        text_rect.width + 20, text_rect.height + 10,
                    )
                    pygame.draw.rect(screen, (30, 30, 30, 170), bg_rect, border_radius=8)
                    pygame.draw.rect(screen, (255, 215, 0), bg_rect, 2, border_radius=8)
                    screen.blit(text_surf, text_rect)
                else:
                    show_level_up = False

        pygame.display.update()
        clock.tick(LEVEL_SPEEDS.get(level, 10))

if __name__ == '__main__':
    main()