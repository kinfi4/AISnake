from agent import GameAIAgent
from game import Game


def train_snake():
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
                #  TODO: save model

            print(f'Game: {agent.n_iterations}, Score: {score}, Record: {record}')

            # TODO: plotting
