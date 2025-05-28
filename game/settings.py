import os

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
CELL_NUMBER_X = WIDTH // CELL_SIZE
CELL_NUMBER_Y = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (220, 0, 0)

FPS = 10

ASSET_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets')