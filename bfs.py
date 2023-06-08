def bfs(state):
    seen = set()
    states = [state]
    round = 0

    while states:
        next_states = []
        for state in states:
            if state.won:
                return (state, round)
            if state.hash in seen:
                continue
            seen.add(state.hash)
            next_states += state.get_next_moves()

        states = next_states
        round += 1
    return None