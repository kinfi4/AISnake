from constants import BLOCK_SIZE, Direction, Point, SCREEN_HEIGHT, SCREEN_WIDTH


class Snake:
    def __init__(self, initial_size=3):
        if initial_size < 1:
            raise ValueError(f'Cant create snake with initial size = {initial_size}')

        self.head = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.blocks = []
        for i in range(initial_size):
            self.blocks.append(Point(self.head.x - i*BLOCK_SIZE, self.head.y))

    def move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
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
