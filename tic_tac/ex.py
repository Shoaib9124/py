# Tic-Tac-Toe full game with Minimax and input/output files

AI = 'X'
HUMAN = 'O'
EMPTY = '_'

# Read board from file
file_path = "input.txt"  # Initial board file
board = []
with open(file_path, "r") as f:
    for line in f:
        row = line.strip().split()
        board.append(row)

# Print board to file
def print_board(b, out_file):
    for row in b:
        out_file.write(" ".join(row) + "\n")
    out_file.write("\n")

# Check if moves are left
def is_moves_left(b):
    for row in b:
        if EMPTY in row:
            return True
    return False

# Evaluate board
def evaluate(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != EMPTY:
            return 10 if b[i][0] == AI else -10
        if b[0][i] == b[1][i] == b[2][i] != EMPTY:
            return 10 if b[0][i] == AI else -10
    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return 10 if b[0][0] == AI else -10
    if b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return 10 if b[0][2] == AI else -10
    return 0

# Minimax function
def minimax(b, depth, is_max):
    score = evaluate(b)
    if score == 10 or score == -10:
        return score
    if not is_moves_left(b):
        return 0

    if is_max:
        best = -1000
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = AI
                    best = max(best, minimax(b, depth + 1, False))
                    b[i][j] = EMPTY
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = HUMAN
                    best = min(best, minimax(b, depth + 1, True))
                    b[i][j] = EMPTY
        return best

# Find best move for AI
def find_best_move(b):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if b[i][j] == EMPTY:
                b[i][j] = AI
                move_val = minimax(b, 0, False)
                b[i][j] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

# Function to let Human play (manual input)
def human_move(b, out_file):
    for i in range(3):
        for j in range(3):
            if b[i][j] == EMPTY:
                b[i][j] = HUMAN
                out_file.write(f"Human chooses position: ({i}, {j})\n")
                return

# Play full game
with open("out.txt", "w") as out:
    out.write("Initial Board:\n")
    print_board(board, out)

    turn = AI  # AI starts
    while is_moves_left(board) and evaluate(board) == 0:
        if turn == AI:
            row, col = find_best_move(board)
            board[row][col] = AI
            out.write(f"AI chooses position: ({row}, {col})\n")
            print_board(board, out)
            turn = HUMAN
        else:
            human_move(board, out)  # currently automated first empty cell
            print_board(board, out)
            turn = AI

    # Final result
    score = evaluate(board)
    if score == 10:
        out.write("AI wins!\n")
    elif score == -10:
        out.write("Human wins!\n")
    else:
        out.write("It's a tie!\n")
