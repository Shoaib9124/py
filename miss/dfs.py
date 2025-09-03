from collections import deque

def is_goal(m_left,c_left,boat,goal):
    return (m_left,c_left,boat)==goal

def is_valid(m_left,c_left):
    m_right = 3 - m_left
    c_right = 3 - c_left
    return (m_left==0 or m_left>=c_left) and (m_right==0 or m_right>=c_right)

moves = [(2,0),(0,2),(1,0),(0,1),(1,1)]

def dfs(start, goal, out):
    stack = [(start, [start])]
    visited = set([start])

    while stack:
        (m_left, c_left, boat), path = stack.pop()

        if is_goal(m_left,c_left,boat,goal):
            out.write("Solution found\n")
            for s in path:
                out.write(str(s)+"\n")
            return True

        for m, c in moves:
            if boat == 1:
                new_state = (m_left - m, c_left - c, 0)
            else:
                new_state = (m_left + m, c_left + c, 1)

            if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3:
                if is_valid(new_state[0], new_state[1]) and new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [new_state]))

    out.write("No solution found\n")
    return False

if __name__=="__main__":
    with open("input.txt") as f:
        lines=f.read().strip().splitlines()
        start = tuple(map(int, lines[0].split()))
        goal = tuple(map(int, lines[1].split()))

    with open("output.txt", "w") as out:
        dfs(start, goal, out)
