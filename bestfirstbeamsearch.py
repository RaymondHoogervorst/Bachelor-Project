import bisect
from queue import PriorityQueue as PQ

def best_first_beam_search_curry(beam_size, heuristic):
    def best_first_beam_search(state):

        nodes_expanded = 0
        seen = set([state.hash])
        
        max_depth = 0
        beam_sizes = [0]

        queue = PQ()
        queue.put((state, 0))

        while queue.qsize() > 0:
            state, steps = queue.get()


            if beam_sizes[steps] >= beam_size:
                continue

            if state.won:
                return (state, steps, nodes_expanded)
            
            beam_sizes[steps] += 1

            if steps == max_depth:
                max_depth += 1
                beam_sizes.append(0)

            if beam_sizes[steps + 1] >= beam_size:
                continue

            nodes_expanded += 1
            for next_state in state.get_next_moves():
                if next_state.hash in seen:
                    continue


                next_state.prev = state
                next_state.score = heuristic(next_state)
                queue.put((next_state, steps + 1))
                seen.add(next_state.hash)

        return (None, None, nodes_expanded)

    return best_first_beam_search


