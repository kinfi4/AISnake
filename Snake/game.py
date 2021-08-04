import random

import pygame

from constants import Colors, BLOCK_SIZE, Point, SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from snake import Snake


pygame.init()
font = pygame.font.SysFont('Arial', 25)


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake')

        self.clock = pygame.time.Clock()

        self.snake, self.score, self.food, self.frame_iteration = None, None, None, None
        self.reset()

    def reset(self):
        self.snake = Snake(initial_size=3)

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.display.get_width() - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.display.get_height() - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.snake.move(action)

        game_over, reward = False, 0
        if self.snake.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.snake.head == self.food:
            self.score += 1
            self._place_food()
            reward = 10
        else:
            self.snake.pop()

        self._update_screen()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def _update_screen(self):
        self.display.fill(Colors.BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, Colors.RED, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, Colors.BLUE, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f'Score: {self.score}', True, Colors.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
