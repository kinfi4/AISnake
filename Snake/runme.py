from agent import GameAIAgent
from game import Game
from plotting import plot


def train_snake():
    plot_scores, plot_mean_scores, total_score, record = [], [], 0, 0
    agent = GameAIAgent()
    game = Game()

    while True:
        # plot(plot_scores, plot_mean_scores)

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
                agent.model.save()

            plot_scores.append(score)
            total_score += score

            mean_score = total_score / agent.n_iterations
            plot_mean_scores.append(mean_score)

            print(f'Game: {agent.n_iterations}, Score: {score}, AVG Score: {round(mean_score, 2)} Record: {record}')


if __name__ == '__main__':
    train_snake()
