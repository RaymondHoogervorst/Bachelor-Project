from time import sleep

def rollout_curry(depth, heuristic):
    def rollout(state, seen = set()):
        try:
            steps_left = depth

            local_seen = []

            while(steps_left > 0):
                if state == None:
                    return (steps_left + 1, 0)
                if state.won:
                    return (-steps_left, 0)
                
                seen.add(state.hash)
                local_seen.append(state.hash)

                state = state.get_random_next_move(seen)
                steps_left -= 1

            if state == None:
                return (1, 0)
            
            return (0, heuristic(state))
        finally:
            for state_hash in local_seen:
                seen.remove(state_hash)
    return rollout

def n_rollout_curry(n_rolls, depth, heuristic):
    rollout = rollout_curry(depth, heuristic)
    return lambda state, seen : min(rollout(state, seen) for _ in range(n_rolls))

def mcts_curry(n_rolls, depth, heuristic):
    rollout = n_rollout_curry(n_rolls, depth, heuristic)

    def mcts(state):
        seen = set()
        round = 0

        while not state.won:
            seen.add(state.hash)
            moves = list(filter(lambda move : move.hash not in seen, state.get_next_moves()))

            if len(moves) == 0:
                return (None, round + 1)

            moves = [(rollout(move, seen), move) for move in moves]
            
            min_move = None
            min_score = (depth + 1, 0)
            for move in moves:
                if move[0] < min_score:
                    min_score, min_move = move

            state = min_move

            round += 1
            # print(round, len(seen))
            # input()

        return (state, round)
    return mcts