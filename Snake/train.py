import argparse

from project_files.agent import GameAIAgent
from project_files.game import Game
from project_files.plotting import plot


def train_snake(file_for_saving, show_plots):
    plot_scores, plot_mean_scores, total_score, record = [], [], 0, 0
    agent = GameAIAgent()
    game = Game()

    while True:
        # get the old state
        old_state = agent.get_state(game)

        move = agent.make_action(old_state)

        # perform move and get new state
        reward, game_over, score = game.step(move)

        # get new state
        new_state = agent.get_state(game)

        agent.train_short_memory(old_state, move, reward, new_state, game_over)
        agent.remember(old_state, move, reward, new_state, game_over)

        if game_over:
            # train long memory, plotting
            game.reset()
            agent.n_iterations += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save(file_for_saving)

            total_score += score

            mean_score = total_score / agent.n_iterations

            if show_plots:
                plot_scores.append(score)
                plot_mean_scores.append(mean_score)

                plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train your snake')
    parser.add_argument('--filename', type=str, help='Path to the file where to save model after training',
                        required=False, default='./model/model.pth')
    parser.add_argument('-s', '--short_form', action='store_false',
                        help='Dont show plotting of scores and mean score while training')

    args = parser.parse_args()

    train_snake(args.filename, args.short_form)
