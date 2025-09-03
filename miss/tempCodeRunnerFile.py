from collections import deque

def is_valid(m_left, c_left):
    m_right = 3 - m_left
    c_right = 3 - c_left
    return (m_left == 0 or m_left >= c_left) and (m_right == 0 or m_right >= c_right)

def dls_missionaries(state, goal, limit, visited, path, out_file):
    if state == goal:
        out_file.write("Solution found (DLS):\n")
        for s in path:
            out_file.write(str(s) + "\n")
        return True
    if limit <= 0:
        return False

    m_left, c_left, boat = state
    moves = [(2,0),(0,2),(1,0),(0,1),(1,1)]
    for m, c in moves:
        if boat == 1:
            new_state = (m_left - m, c_left - c, 0)
        else:
            new_state = (m_left + m, c_left + c, 1)

        if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3:
            if is_valid(new_state[0], new_state[1]) and new_state not in visited:
                visited.add(new_state)
                if dls_missionaries(new_state, goal, limit-1, visited, path + [new_state], out_file):
                    return True
                visited.remove(new_state)
    return False

def ids_missionaries(start, goal, max_depth, out_file):
    for depth in range(max_depth+1):
        visited = set([start])
        if dls_missionaries(start, goal, depth, visited, [start], out_file):
            return True
    out_file.write("No solution found (IDS).\n")
    return False


if __name__=="__main__":
    with open("input_l.txt") as f:
        lines=f.read().strip().splitlines()

    limit=int(lines[0].strip())
    start=tuple(map(int,lines[1].split()))
    goal=tuple(map(int,lines[2].split()))

    with open("output_ids.txt","w") as out:
        ids_missionaries(start,goal,limit,out)
