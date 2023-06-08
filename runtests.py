import gamestate
from beamsearch import beam_search_curry
from bestfirstbeamsearch import best_first_beam_search_curry
from mcts import mcts_curry
from time import time_ns
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
for i in range(13):
    n = 2**i
    print(f"RUNNING FOR SIZE {n}")

    search = best_first_beam_search_curry(n, gamestate.n_blocking_base)
    run_tests(parsed, search, f"depthfirstbeam{n}")
    print("1/2")

    search = best_first_beam_search_curry(n, gamestate.n_blocking_recursive)
    run_tests(parsed, search, f"Rdepthfirstbeam{n}")
    print("2/2")