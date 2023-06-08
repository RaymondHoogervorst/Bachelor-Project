from results.analysis import *
from openpyxl import load_workbook

excel_file = load_workbook('benchmarking.xlsx')

def get_configurations(algo, type):

    if type == "beam":
        for i in range(4,13):
            n = 2**i
            yield f'{n}'
    elif type == "mcts":
        for n_rolls in (1, 5, 10):
            for depth in (1, 5, 10):
                yield f'{n_rolls}x{depth}'

def get_configuration_length(type):
    return 2 if type == "mcts" else 1


def analyse_on_benchmark(algo, type, benchmark, criteria, inverse):
    best_score = None
    best_config = None
    best_heuristic = None

    for config in get_configurations(algo, type):
        for heuristic, prefix in heuristics:

            filename = f'results/{prefix}{algo}{config}.csv'

            runtime = get_avg_runtime(filename)

            if runtime > benchmark:
                continue

            score = criteria(filename)

            if inverse:
                normal_score = -score
            else:
                normal_score = score

            if best_score == None or normal_score > best_score:
                best_score = normal_score
                best_config = config
                best_heuristic = heuristic
    
    return (
        best_config,
        best_heuristic,
        -best_score if inverse else best_score,
    )

algorithms = [
    ("depthfirstbeam", "beam", ord('I')),
    ("mcts", "mcts", ord('B')),
    ("beam", "beam", ord('F')),
]

criteria = [
    ("avg_distance", True),
    ("success_rate", False),
]

heuristics = [
    ('recursive', 'R'),
    ('base', '')
]

TABLE_START_Y = 3

factors = (0.25, 0.5, 0.75, 1)
rows = range(TABLE_START_Y, TABLE_START_Y + len(factors))

benchmark = get_avg_runtime("results/bfs.csv")

for criterion, inverse in criteria:
    sheet = excel_file[criterion]
    def write_cell(y, x, value):
        sheet[f'{chr(x)}{y}'] = value

    for factor, y in zip(factors, rows):
        for algo, type, x in algorithms:
            best_config,best_heuristic, best_score = analyse_on_benchmark(
                algo, type, benchmark * factor, globals()[f'get_{criterion}'], inverse
            )

            width = get_configuration_length(type) + 2

            if best_config != None:
                config = best_config.split('x')

                write_cell(y, x, best_score)
                write_cell(y, x + width - 1, best_heuristic)

                for i, value in enumerate(config):
                    write_cell(y, x + i + 1, value)

                print(f'\t\t{criterion}: {best_config} {best_score}')
            else:
                write_cell(y, x, 'N/A')

                print(f'\t\t{criterion}: ALL CONFIGS FAILED')

excel_file.save('benchmarking.xlsx')