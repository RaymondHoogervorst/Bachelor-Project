import csv
import glob, os
import matplotlib.pyplot as plt

PADDING = 0.1

UNITS = {
    'avg_runtime': 'ms',
}

def analysis(filename, iter):
    with open(filename, 'r') as fp:
        r = csv.reader(fp)
        r.__next__()
        for line in r:
            iter(line)

def get_ratio_to_optimal(filename):
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

def get_avg_expanded(filename):
    total = 0
    n = 0

    def iter(line):
        nonlocal n, total

        n += 1
        total += int(line[5])

    analysis(filename, iter)
    return total / n

# NODES_EXPANDED_BASELINE = get_avg_expanded("results/bfs.csv")
RUNTIME_BASELINE = get_avg_runtime("results/bfs.csv")

result = {
    "depthfirstbeam": {
        'ratio_to_optimal': [],
        'success_rate': [],
        'avg_runtime': [],
        'nodes_expanded': [],
    },
    "beam": {
        'ratio_to_optimal': [],
        'success_rate': [],
        'avg_runtime': [],
        'nodes_expanded': [],
    },
    "Rdepthfirstbeam": {
        'ratio_to_optimal': [],
        'success_rate': [],
        'avg_runtime': [],
        'nodes_expanded': [],
    },
    "Rbeam": {
        'ratio_to_optimal': [],
        'success_rate': [],
        'avg_runtime': [],
        'nodes_expanded': [],
    },
}

beam_widths = [2**i for i in range(13)]

for i in range(13):
    n = 2**i

    for key in ["depthfirstbeam", "beam", "Rdepthfirstbeam", "Rbeam"]:
        filename = f"results/{key}{n}.csv"
        if not os.path.exists(filename):
            raise Exception(f"File {filename} does not exist")

        result[key]['ratio_to_optimal'].append(get_ratio_to_optimal(filename))
        result[key]['success_rate'].append(get_success_rate(filename))
        result[key]['avg_runtime'].append(get_avg_runtime(filename))
        result[key]['nodes_expanded'].append(get_avg_expanded(filename))

AXIS_LABEL_SIZE = 12

def plotAlgo(algo, value, isBottom, isRight):
    ax = plt.subplot(2, 2, 1 + 2 * isBottom + isRight)

    Ralgo = 'R' + algo
    plt.plot(beam_widths, result[algo][value], label="Base heuristic")
    plt.plot(beam_widths, result[Ralgo][value], label="Recursive heuristic")

    # if algo == "beam":
    #     if value == "avg_runtime":
    #         plt.axhline(RUNTIME_BASELINE, label="Breath First Search", color="red", linestyle="-")
        # elif value == "nodes_expanded":
        #     plt.axhline(NODES_EXPANDED_BASELINE, label="Breath First Search", color="red", linestyle="-")

    if value == 'success_rate':
        ax.set_ylim(0, 1.1)
    elif value == 'ratio_to_optimal':
        ax.set_ylim(0.9, 5.5)


    if isRight:
        ax.yaxis.set_label_position('right')
        ax.yaxis.tick_right()
    
    if not isBottom:
        ax.xaxis.set_label_position('top')
        ax.xaxis.tick_top()

    plt.xlabel("Beam Width", fontsize=AXIS_LABEL_SIZE)

    if unit := UNITS.get(value):
        plt.ylabel(f"{value} ({unit})", fontsize=AXIS_LABEL_SIZE)
    else:
        plt.ylabel(value, fontsize=AXIS_LABEL_SIZE)

    plt.show()

def plot_features(feature1, feature2, resultname):
    fig, axs = plt.subplots(2, 2)
    fig.align_labels()

    plotAlgo("beam", feature1, 0, 0)
    plotAlgo("depthfirstbeam", feature1, 0, 1, )
    plotAlgo("beam", feature2, 1, 0)
    plotAlgo("depthfirstbeam", feature2, 1, 1)

    plt.legend(loc=4)
    plt.subplots_adjust(wspace=PADDING, hspace=PADDING)
    title = ' ' * 19 + 'Beam Search    Best First Beam Search'

    plt.subplots_adjust(top=0.82)
    plt.suptitle(title, fontweight='bold')



    plt.savefig(f"results_figures/{resultname}.png")
    plt.close()

# plot_features("ratio_to_optimal", "success_rate", "solution_quality")
# plot_features("avg_runtime", "nodes_expanded", "performance")

print(get_avg_expanded("results/depthfirstbeam2048.csv"))
print(get_avg_expanded("results/Rdepthfirstbeam2048.csv"))

# for i in range(13):
#     n = 2**i
#     # print(n)
#     print(get_success_rate(f"results/depthfirstbeam{n}.csv"))
    