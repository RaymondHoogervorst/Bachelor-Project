import csv
import numpy as np
import matplotlib.pyplot as plt

AXIS_LABEL_SIZE = 14
TICK_LABEL_SIZE = 11

def analysis(filename, iter):
    with open(filename, 'r') as fp:
        r = csv.reader(fp)
        r.__next__()
        for line in r:
            iter(line)

def get_avg_distance(filename):
    optimal = 0
    real = 0

    def iter(line):
        nonlocal optimal, real
        if not line[3]:
            return

        optimal += int(line[1])
        real += int(line[3])

    analysis(filename, iter)
    return real / optimal

def get_success_rate(filename):
    success = 0
    total = 0

    def iter(line):
        nonlocal success, total
        total += 1
        success += bool(line[3])

    analysis(filename, iter)
    return success / total

def get_avg_runtime(filename):
    total = 0
    n = 0

    def iter(line):
        nonlocal n, total

        n += 1
        total += int(line[4]) / 1_000_000

    analysis(filename, iter)
    return total / n

def graph_stat(stat, algo, title = None):

    IS_RUNTIME = stat == 'avg_runtime'

    if IS_RUNTIME:
        BASELINE = 115.5

    values = [1, 5, 10]

    function = globals()[f'get_{stat}']


    # Make a bar graph, with the height of each bar being the property, a bar for each n_rolls and depth combo, grouped by n_rolls

    TOTAL_WIDTH = 100
    BAR_WIDTH = 5

    # plt.bar([x for _, x in stats], [y for y, _ in stats], width=BAR_WIDTH)


    values = [1, 5, 10]

    group_centers = np.arange(TOTAL_WIDTH / (len(values) + 1), TOTAL_WIDTH, TOTAL_WIDTH / (len(values) + 1))

    for offset, n_rolls in zip([-1, 0, 1], values):
        y = [function(f'results/{algo}{n_rolls}x{depth}.csv') for depth in values]
        plt.bar(group_centers + offset * BAR_WIDTH, y, width=BAR_WIDTH, label=f'n_rolls of {n_rolls}')


    plt.xlim(0, TOTAL_WIDTH)
    plt.xticks(group_centers, [f'{value} moves' for value in values], fontsize=TICK_LABEL_SIZE)
    plt.yticks(fontsize=TICK_LABEL_SIZE)
    plt.xlabel('rollout depth', fontsize=AXIS_LABEL_SIZE)
    plt.ylabel(stat if stat != 'avg_distance' else 'ratio to optimal', fontsize=AXIS_LABEL_SIZE)

    if IS_RUNTIME:
        plt.axhline(y=BASELINE, color='r', linestyle='-', label='breadth first search')

    plt.legend(loc=2 if stat == 'avg_runtime' else 3)

    # plt.savefig(f'results/{algo}_{stat}.png')
    # plt.close()

# print(get_avg_runtime('results/bfs.csv'))

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
graph_stat('success_rate', 'mcts', 'Monte Carlo Tree Search + base heuristic')
plt.subplot(1, 3, 2)
graph_stat('avg_distance', 'mcts', 'Monte Carlo Tree Search + base heuristic')
plt.subplot(1, 3, 3)
graph_stat('avg_runtime', 'mcts', 'Monte Carlo Tree Search + base heuristic')

plt.savefig('results_figures/mcts.png', bbox_inches='tight')
plt.close()

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
graph_stat('success_rate', 'Rmcts', 'Monte Carlo Tree Search + recursive heuristic')
plt.subplot(1, 3, 2)
graph_stat('avg_distance', 'Rmcts', 'Monte Carlo Tree Search + recursive heuristic')
plt.subplot(1, 3, 3)
graph_stat('avg_runtime', 'Rmcts', 'Monte Carlo Tree Search + recursive heuristic')

plt.savefig('results_figures/Rmcts.png', bbox_inches='tight')