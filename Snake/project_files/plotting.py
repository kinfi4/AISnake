import matplotlib.pyplot as plt
from IPython import display


plt.ion()


def plot(scores, mean_scores):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of games')
    plt.ylabel('Score')
    plt.plot(scores, label='scores')
    plt.plot(mean_scores, label='mean score')
    plt.ylim(ymin=0)

    plt.legend()

    try:
        plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
        plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    except IndexError:
        pass

    plt.show(block=False)
    plt.pause(0.000001)
