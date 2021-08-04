import numpy as np

from constants import BLOCK_SIZE, Direction, Point, SCREEN_HEIGHT, SCREEN_WIDTH


class Snake:
    def __init__(self, initial_size=3):
        if initial_size < 1:
            raise ValueError(f'Cant create snake with initial size = {initial_size}')

        self.head = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.direction = Direction.RIGHT

        self.blocks = []
        for i in range(initial_size):
            self.blocks.append(Point(self.head.x - i*BLOCK_SIZE, self.head.y))

    def move(self, action):
        # action = [straight, right, left]
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        cur_dir_index = directions.index(self.direction)

        x = self.head.x
        y = self.head.y

        new_direction = None
        if np.array_equal(action, [1, 0, 0]):  # Go straight, no directions change
            new_direction = directions[cur_dir_index]
        elif np.array_equal(action, [0, 1, 0]):  # right turn, r -> d -> l -> u
            new_dir_index = (cur_dir_index + 1) % 4
            new_direction = directions[new_dir_index]
        elif np.array_equal(action, [0, 0, 1]):  # left turn, r -> u -> l -> d
            new_dir_index = (cur_dir_index - 1) % 4
            new_direction = directions[new_dir_index]

        self.direction = new_direction

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)
        self.blocks.insert(0, self.head)

    def pop(self):
        self.blocks.pop()

    def is_collision(self):
        return self._hit_boundary() or self.head in self.blocks[1:]

    def _hit_boundary(self):
        return self.head.x > SCREEN_WIDTH - BLOCK_SIZE \
               or self.head.x < 0 \
               or self.head.y > SCREEN_HEIGHT - BLOCK_SIZE \
               or self.head.y < 0

    def __contains__(self, item):
        return item in self.blocks

    def __iter__(self):
        for point in self.blocks:
            yield point

    def __len__(self):
        return len(self.blocks)
