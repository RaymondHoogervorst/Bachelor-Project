def beam_search_curry(beam_size, heuristic):
    def beam_search(state):
        nodes_expanded = 0

        seen = set()
        states = [(state, None)]
        round = 0
        while states:
            next_states = []
            for state, _ in states:
                if state.won:
                    return (state, round, nodes_expanded)
                if state.hash in seen:
                    continue
                seen.add(state.hash)

                nodes_expanded += 1
                next_moves = state.get_next_moves()
                for next_state in next_moves:
                    if next_state.won:
                        next_score = -1
                    else:
                        next_score = heuristic(next_state)
                    next_state.prev = state
                    next_states.append((next_state, next_score))
            next_states.sort(key=lambda x: x[1])
            
            states = next_states[:beam_size]
            round += 1
        return (None, None, nodes_expanded)
    return beam_search
