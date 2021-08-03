import random

import pygame

from constants import Colors, BLOCK_SIZE, Direction, Point, SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from snake import Snake


pygame.init()
font = pygame.font.SysFont('Arial', 25)


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake')

        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT

        self.snake = Snake()

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.display.get_width() - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.display.get_height() - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP

        self.snake.move(self.direction)

        game_over = False
        if self.snake.is_collision():
            game_over = True
            return game_over, self.score

        if self.snake.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_screen()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _update_screen(self):
        self.display.fill(Colors.BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, Colors.RED, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, Colors.BLUE, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f'Score: {self.score}', True, Colors.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()

    while True:
        is_end, score = game.step()

        if is_end:
            break

    pygame.quit()
