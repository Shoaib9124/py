from collections import deque

# ---------- VALID STATE ----------
def is_valid(m_left, c_left):
    m_right = 3 - m_left
    c_right = 3 - c_left
    return (m_left == 0 or m_left >= c_left) and (m_right == 0 or m_right >= c_right)

# ---------- ILS ----------
def ils_missionaries(start, goal, limit, cost_map, out_file):
    def dls_cost(state, remaining_limit, path, cumulative_cost, visited):
        if state == goal:
            out_file.write("Solution found (ILS):\n")
            for step, (s, move_cost) in enumerate(path[1:], 1):  # skip initial state cost 0
                out_file.write(f"Step {step}: {s}, move cost: {move_cost}\n")
            out_file.write(f"Total cost: {cumulative_cost}\n")
            return True

        m_left, c_left, boat = state
        moves = [(2,0),(0,2),(1,0),(0,1),(1,1)]

        for m, c in moves:
            if boat == 1:  # boat on left
                new_state = (m_left - m, c_left - c, 0)
            else:  # boat on right
                new_state = (m_left + m, c_left + c, 1)

            if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3 and is_valid(new_state[0], new_state[1]):
                move_cost = cost_map.get((m, c), 1)
                if new_state not in visited and remaining_limit - move_cost >= 0:
                    visited.add(new_state)
                    if dls_cost(new_state, remaining_limit - move_cost,
                                path + [(new_state, move_cost)],
                                cumulative_cost + move_cost,
                                visited):
                        return True
                    visited.remove(new_state)
        return False

    for l in range(1, limit + 1):
        visited = set([start])
        if dls_cost(start, l, [(start, 0)], 0, visited):
            return True
    out_file.write("No solution found (ILS).\n")
    return False

# ---------- MAIN ----------
if __name__=="__main__":
    with open("input_cost.txt") as f:
        lines = f.read().strip().splitlines()
        start = tuple(map(int, lines[0].split()))
        goal = tuple(map(int, lines[1].split()))
        cost_map = {}
        if len(lines) > 2:
            for item in lines[2].split():
                key, value = item.split(":")
                m, c = map(int, key.split(","))
                cost_map[(m, c)] = int(value)
        limit = int(lines[3]) if len(lines) > 3 else 10

    with open("output_ils.txt", "w") as out:
        ils_missionaries(start, goal, limit, cost_map, out)
