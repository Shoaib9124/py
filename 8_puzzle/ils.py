from collections import deque

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

def dls_with_cost(start, goal, x, y, move_costs, file, cost_limit):
    # stack: (matrix, x, y, current_cost, path)
    stack = [(start, x, y, 0, [])]
    vis = {tuple(map(tuple, start))}

    while stack:
        matrix, dx, dy, current_cost, path = stack.pop()

        if is_goal(matrix, goal):
            file.write("Solution found!\n\n")
            file.write("Steps:\n")
            for step, (move, state, cost) in enumerate(path, 1):
                file.write(f"Step {step}: Move {move}, Cost = {cost}\n")
                print_matrix(state, file)
            file.write(f"Total Cost: {current_cost}\n")
            return True

        for i in range(4):
            nrow, ncol = dx + row[i], dy + col[i]
            if is_valid(nrow, ncol):
                new_matrix = [r[:] for r in matrix]
                new_matrix[dx][dy], new_matrix[nrow][ncol] = new_matrix[nrow][ncol], new_matrix[dx][dy]

                next_cost = current_cost + move_costs[i]
                if next_cost > cost_limit:
                    continue

                state_tuple = tuple(map(tuple, new_matrix))
                if state_tuple not in vis:
                    vis.add(state_tuple)
                    stack.append((new_matrix, nrow, ncol, next_cost, path + [(move_names[i], new_matrix, move_costs[i])]))

    return False

def ils(start, goal, x, y, move_costs, out, max_cost=20):
    for limit in range(max_cost + 1):
        out.write(f"\nTrying cost limit = {limit}\n")
        if dls_with_cost(start, goal, x, y, move_costs, out, limit):
            out.write(f"Goal found at cost {limit}\n")
            return True
    return False

if __name__ == "__main__":
    with open("input_cost.txt") as f:
        lines = f.read().strip().splitlines()

    max_cost = int(lines[0].strip())
    move_costs = list(map(int, lines[1].split()))  # e.g., "2 3 1 4" for Up, Down, Left, Right

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

    with open("output_ils.txt", "w") as out:
        found = ils(start, goal, x, y, move_costs, out, max_cost)
        if not found:
            out.write("Goal not found within given cost limit\n")
