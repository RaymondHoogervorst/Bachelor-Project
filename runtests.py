import gamestate
from beamsearch import beam_search_curry
from bestfirstbeamsearch import best_first_beam_search_curry
from mcts import mcts_curry
from time import time_ns
import matplotlib.pyplot as plt
import csv

# search = mcts_curry(1, 5, gamestate.n_blocking_base)

def run_tests(lines, search, filename = None):

    with open("results/" + filename + ".csv", 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["Code", "Optimal-Steps", "Tree-size", "Steps", "Time", "Expanded"])

        for line in lines:
            (steps, code, width, state) = line
            row = [code, steps, width]

            runtime = -time_ns()
            final = search(state)
            runtime += time_ns()

            state, steps, expanded = final
            row += [steps if state != None else '', runtime, expanded]

            writer.writerow(row)

with open('games/solvable.txt', 'r') as fp:
    lines = fp.readlines()

parsed = []
lines = lines[::50]

for line in lines:
    (steps, code, width) = line.strip().split(' ')
    state = gamestate.GameState.parse(code)
    parsed.append((steps, code, width, state))

print("Parsed")


def calc_histograms():
    optimal_lengths = [int(x[0]) for x in parsed]

    def hist(x, filename, label):
        max_x = max(x for x in x if x != None)

        print(sum(n < 3 for n in x) / len(parsed))

        print(min(x))
        plt.hist(x, bins=100, density=True, label=label, range=(1, 25))
        plt.ylabel("Frequency (%)")
        plt.xlabel("Ratio to optimal")

        plt.savefig("length_distro/" + filename + ".png")

    algorithms_to_compare = (
        ("Rmcts1x1", "Monte Carlo Tree Search (1x1)"),
        # ("beam4096", "Beam Search (4096)"),
        # ("Rdepthfirstbeam2048", "Depth First Beam Search (2048)"),
    )

    # hist(optimal_lengths, "optimal")

    for (filename, label) in algorithms_to_compare:
        with open("results/" + filename + ".csv", 'r') as f:
            reader = csv.reader(f)
            next(reader)
            # ratio = [int(row[3]) / int(row[1]) if row[3] != '' else -1 for row in reader]
            ratio = [int(row[3]) / int(row[1]) for row in reader if row[3] != '']
            hist(ratio, filename, label)

    plt.legend()

def calc_tree_width_comparison():
    algorithms = (
        ("beam4096", "Beam Search (4096)"),
        # ("Rdepthfirstbeam2048", "Depth First Beam Search (2048)"),
    )

    for (filename, label) in algorithms:
        with open("results/" + filename + ".csv", 'r') as f:
            reader = csv.reader(f)
            next(reader)

            reader = [row for row in reader if row[3] != '']

            tree_sizes = [int(row[2]) for row in reader if row[3] != '']
            optimal_lengths = [int(row[1]) for row in reader if row[3] != '']
            solution_lengths = [int(row[3]) for row in reader if row[3] != '']

            tree_ratio = [y / x for (x, y) in zip(tree_sizes, optimal_lengths)]
            solution_ratio = [y / x for (x, y) in zip(optimal_lengths, solution_lengths)]

            plt.scatter(tree_ratio, solution_ratio, label=label, alpha=0.5	)

    plt.legend()
    plt.savefig("tree_width_comparison.png")



# calc_tree_width_comparison()
# calc_histograms()

# for i in range(13):
#     n = 2**i
#     print(f"RUNNING FOR SIZE {n}")

#     search = best_first_beam_search_curry(n, gamestate.n_blocking_base)
#     run_tests(parsed, search, f"depthfirstbeam{n}")
#     print("1/2")

#     search = best_first_beam_search_curry(n, gamestate.n_blocking_recursive)
#     run_tests(parsed, search, f"Rdepthfirstbeam{n}")
#     print("2/2")