from constants import Colors, BLOCK_SIZE, Direction, Point, SPEED, SCREEN_HEIGHT, SCREEN_WIDTH


class Snake:
    def __init__(self, initial_size=3):
        if initial_size < 1:
            raise ValueError(f'Cant create snake with initial size = {initial_size}')

        self.head = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.blocks = []
        for i in range(initial_size):
            self.blocks.append(Point(self.head.x - i*BLOCK_SIZE, self.head.y))

