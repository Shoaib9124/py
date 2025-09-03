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

def dls(start, goal, x, y, file, limit):
    # stack holds: (matrix, x, y, depth, path)
    stack = [(start, x, y, 0, [])]
    vis = {tuple(map(tuple, start))}

    while stack:
        matrix, dx, dy, depth, path = stack.pop()

        if is_goal(matrix, goal):
            file.write("Solution found!\n\n")
            file.write("Steps:\n")
            for step, (move, state) in enumerate(path, 1):
                file.write(f"Move {step}: {move}\n")
                print_matrix(state, file)
            return True

        if depth >= limit:
            continue

        for i in range(4):
            nrow, ncol = dx + row[i], dy + col[i]
            if is_valid(nrow, ncol):
                new_matrix = [r[:] for r in matrix]
                new_matrix[dx][dy], new_matrix[nrow][ncol] = new_matrix[nrow][ncol], new_matrix[dx][dy]

                state = tuple(map(tuple, new_matrix))
                if state not in vis:
                    vis.add(state)
                    stack.append((new_matrix, nrow, ncol, depth + 1, path + [(move_names[i], new_matrix)]))

    return False


if __name__ == "__main__":
    with open("input_l.txt") as f:
        lines = f.read().strip().splitlines()

    limit = int(lines[0].strip())

    start = [list(map(int, lines[1].split())),
             list(map(int, lines[2].split())),
             list(map(int, lines[3].split()))]

    goal = [list(map(int, lines[4].split())),
            list(map(int, lines[5].split())),
            list(map(int, lines[6].split()))]

    x = y = 0
    for i in range(3):
        for j in range(3):
            if start[i][j] == 0:
                x, y = i, j

    with open("output_dls.txt", "w") as out:
        found = dls(start, goal, x, y, out, limit)
        if not found:
            out.write("Goal not found with given limit")
