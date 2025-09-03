import heapq

# ---------- VALID STATE ----------
def is_valid(m_left, c_left):
    m_right = 3 - m_left
    c_right = 3 - c_left
    return (m_left == 0 or m_left >= c_left) and (m_right == 0 or m_right >= c_right)

# ---------- UCS ----------
def ucs_missionaries(start, goal, cost_map, out_file):
    pq = [(0, start, [(start, 0)])]  # (cumulative_cost, state, path)
    visited = {}

    moves = [(2,0),(0,2),(1,0),(0,1),(1,1)]

    while pq:
        cum_cost, (m_left, c_left, boat), path = heapq.heappop(pq)

        if (m_left, c_left, boat) == goal:
            out_file.write("Solution found (UCS):\n")
            for step, (s, move_cost) in enumerate(path[1:], 1):
                out_file.write(f"Step {step}: {s}, move cost: {move_cost}\n")
            out_file.write(f"Total cost: {cum_cost}\n")
            return True

        if (m_left, c_left, boat) in visited and visited[(m_left, c_left, boat)] <= cum_cost:
            continue
        visited[(m_left, c_left, boat)] = cum_cost

        for m, c in moves:
            if boat == 1:  # boat on left
                new_state = (m_left - m, c_left - c, 0)
            else:  # boat on right
                new_state = (m_left + m, c_left + c, 1)

            if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3 and is_valid(new_state[0], new_state[1]):
                move_cost = cost_map.get((m, c), 1)
                heapq.heappush(pq, (cum_cost + move_cost, new_state, path + [(new_state, move_cost)]))

    out_file.write("No solution found (UCS).\n")
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

    with open("output_ucs.txt", "w") as out:
        ucs_missionaries(start, goal, cost_map, out)
