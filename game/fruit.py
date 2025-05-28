import random
from settings import WIDTH, HEIGHT, CELL_SIZE

class Fruit:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            pos = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
            if pos not in snake_body:
                self.position = pos
                return pos

    def get_pos(self):
        return self.position