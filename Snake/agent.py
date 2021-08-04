import random
from collections import deque

import numpy as np
import torch

from game import Game
from model import Trainer, Model
from constants import Direction, Point, MAX_MEMORY, BATCH_SIZE, BLOCK_SIZE, MUTATION_RATE


class GameAIAgent:
    def __init__(self):
        self.n_iterations = 0
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = Model(11, 256, 3)
        self.trainer = Trainer(self.model)

    @staticmethod
    def get_state(game: Game):
        head = game.snake.head
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_is_r = game.snake.direction == Direction.RIGHT
        dir_is_l = game.snake.direction == Direction.LEFT
        dir_is_u = game.snake.direction == Direction.UP
        dir_is_d = game.snake.direction == Direction.DOWN

        state = [
            # danger straight
            (dir_is_r and game.snake.is_collision(point_r))
            or (dir_is_l and game.snake.is_collision(point_l))
            or (dir_is_u and game.snake.is_collision(point_u))
            or (dir_is_d and game.snake.is_collision(point_d)),

            # danger right
            (dir_is_r and game.snake.is_collision(point_d))
            or (dir_is_l and game.snake.is_collision(point_u))
            or (dir_is_u and game.snake.is_collision(point_r))
            or (dir_is_d and game.snake.is_collision(point_l)),

            # danger left
            (dir_is_r and game.snake.is_collision(point_u))
            or (dir_is_l and game.snake.is_collision(point_d))
            or (dir_is_u and game.snake.is_collision(point_l))
            or (dir_is_d and game.snake.is_collision(point_r)),

            # move direction
            dir_is_l,
            dir_is_r,
            dir_is_u,
            dir_is_d,

            # food location
            game.food.x < game.snake.head.x,  # food left
            game.food.x > game.snake.head.x,  # food right
            game.food.y < game.snake.head.y,  # food up
            game.food.y > game.snake.head.y  # food down
        ]

        return np.array(state, dtype=np.int32)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        memory_samples = random.sample(self.memory, BATCH_SIZE) if len(self.memory) > BATCH_SIZE else list(self.memory)

        states, actions, rewards, next_states, game_overs = zip(*memory_samples)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def make_action(self, state):
        final_move = [0, 0, 0]

        if random.randint(0, 200) < MUTATION_RATE - self.n_iterations:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            predictions = self.model(torch.tensor(state, dtype=torch.float))
            move = torch.argmax(predictions).item()
            final_move[move] = 1

        return final_move
