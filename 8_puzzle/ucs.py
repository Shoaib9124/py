import heapq

row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]
move_names = ["Up", "Down", "Left", "Right"]

def print_matrix(matrix, file):
    for r in matrix:
        file.write(" ".join(map(str, r)) + "\n")
    file.write("\n")

def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def is_goal(matrix, goal):
    return matrix == goal

def ucs(start, goal, x, y, move_costs, out):
    # Priority queue: (total_cost, matrix, x, y, path)
    heap = [(0, start, x, y, [])]
    visited = set()

    while heap:
        cost, matrix, dx, dy, path = heapq.heappop(heap)

        state_tuple = tuple(map(tuple, matrix))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if is_goal(matrix, goal):
            out.write("Solution found!\n\n")
            out.write("Steps:\n")
            for step, (move, state, move_cost) in enumerate(path, 1):
                out.write(f"Step {step}: Move {move}, Cost = {move_cost}\n")
                print_matrix(state, out)
            out.write(f"Total Cost: {cost}\n")
            return True

        for i in range(4):
            nrow, ncol = dx + row[i], dy + col[i]
            if is_valid(nrow, ncol):
                new_matrix = [r[:] for r in matrix]
                new_matrix[dx][dy], new_matrix[nrow][ncol] = new_matrix[nrow][ncol], new_matrix[dx][dy]
                next_cost = cost + move_costs[i]
                heapq.heappush(heap, (next_cost, new_matrix, nrow, ncol, path + [(move_names[i], new_matrix, move_costs[i])]))

    out.write("Goal not reachable\n")
    return False

if __name__ == "__main__":
    with open("input_cost.txt") as f:
        lines = f.read().strip().splitlines()

    max_cost = int(lines[0].strip())         # optional, could ignore for UCS
    move_costs = list(map(int, lines[1].split()))  # Up, Down, Left, Right

    start = [list(map(int, lines[2].split())),
             list(map(int, lines[3].split())),
             list(map(int, lines[4].split()))]

    goal = [list(map(int, lines[5].split())),
            list(map(int, lines[6].split())),
            list(map(int, lines[7].split()))]

    x = y = 0
    for i in range(3):
        for j in range(3):
            if start[i][j] == 0:
                x, y = i, j

    with open("output_ucs.txt", "w") as out:
        ucs(start, goal, x, y, move_costs, out)
