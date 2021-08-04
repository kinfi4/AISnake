from collections import namedtuple
from enum import Enum


BLOCK_SIZE = 20
SPEED = 5
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
MUTATION_RATE = 100   # the higher this rate the more likely snake will "mutate" (make random moves not based on NN)

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

Point = namedtuple('Point', 'x y')


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (200, 30, 30)
    BLUE = (30, 30, 200)


class Direction(Enum):
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    UP = 'UP'
    DOWN = 'DOWN'
