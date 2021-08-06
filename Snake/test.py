import argparse

import torch

from project_files.model import Model
from project_files.game import Game
from project_files.agent import GameAIAgent


class SnakePlayer:
    def __init__(self, model_file_path):
        model = Model(11, 256, 3)
        model.load_state_dict(torch.load(model_file_path))
        model.eval()

        self.model = model
        self.agent = GameAIAgent()

    def play_snake(self, speed):
        total_score, record = 0, 0
        game = Game(speed=speed)

        while True:
            state = self.agent.get_state(game)
            move = self._make_prediction(state)

            reward, game_over, score = game.step(move)

            if game_over:
                self.agent.n_iterations += 1
                total_score += score
                record = max(score, record)
                mean_score = round(total_score / self.agent.n_iterations, 2)

                game.reset()
                print(f'Game: {self.agent.n_iterations}, Score: {score}, Mean Score: {mean_score}, Record: {record}')

    def _make_prediction(self, state):
        final_move = [0, 0, 0]
        predictions = self.model(torch.tensor(state, dtype=torch.float))
        move = torch.argmax(predictions).item()
        final_move[move] = 1

        return final_move


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model_file', help='Path to the model')
    parser.add_argument('-s', '--speed', type=int, help='The speed of snake', default=30)

    args = parser.parse_args()

    player = SnakePlayer(args.model_file)
    player.play_snake(args.speed)
