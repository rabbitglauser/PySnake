import pygame
from settings import CELL_SIZE

class Snake:
    def __init__(self, images):
        x = 600 // 2
        y = 400 // 2
        self.body = [
            [x, y],
            [x - CELL_SIZE, y],
            [x - 2*CELL_SIZE, y]
        ]
        self.direction = 'RIGHT'
        self.images = images

    def reset(self):
        x = 600 // 2
        y = 400 // 2
        self.body = [
            [x, y],
            [x - CELL_SIZE, y],
            [x - 2*CELL_SIZE, y]
        ]
        self.direction = 'RIGHT'

    def move(self, change_to):
        self.direction = change_to
        head = self.body[0][:]
        if self.direction == 'UP':
            head[1] -= CELL_SIZE
        elif self.direction == 'DOWN':
            head[1] += CELL_SIZE
        elif self.direction == 'LEFT':
            head[0] -= CELL_SIZE
        elif self.direction == 'RIGHT':
            head[0] += CELL_SIZE
        self.body.insert(0, head)

    def shrink(self):
        self.body.pop()

    def get_head_pos(self):
        return self.body[0]

    def get_body(self):
        return self.body

    def draw(self, screen):
        snake_body = self.body
        images = self.images
        for i, segment in enumerate(snake_body):
            x, y = segment
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