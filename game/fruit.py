import random
from settings import WIDTH, HEIGHT, CELL_SIZE

class Fruit:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, occupied_positions):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            pos = (x, y)
            if pos not in occupied_positions:
                self.position = pos
                return pos

    def get_pos(self):
        return self.position
