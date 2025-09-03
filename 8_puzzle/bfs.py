from collections import deque
import os

row=[-1,1,0,0]
col=[0,0,-1,1]

def print_matrix(matrix,file):
    for r in matrix:
        file.write(" ".join(map(str,r))+"\n")
    file.write("\n")

def is_valid(x,y):
    return 0<=x<3 and 0<=y<3

def is_goal(matrix,goal):
    return matrix==goal

def bfs(start,goal,x,y,file):

    q=deque([(start,x,y,0)])
    visited=set([tuple(map(tuple,start))])

    while q:
        matrix,dx,dy,depth=q.popleft()

        file.write(f"current depth{depth}\n")
        print_matrix(matrix,file)

        if is_goal(matrix,goal):
            file.write("res found")
            return
        
        for i in range(4):
            nrow,ncol=dx+row[i],dy+col[i]
            if is_valid(nrow,ncol):
                new_matrix=[r[:] for r in matrix]
                new_matrix[dx][dy],new_matrix[nrow][ncol]=new_matrix[nrow][ncol],new_matrix[dx][dy]

                state=tuple(map(tuple,new_matrix))
                if state not in visited:
                    q.append((new_matrix,nrow,ncol,depth+1))
                    visited.add(state)


    file.write("no solution found")


if __name__=="__main__":
    with open("input.txt") as f:
        lines=f.read().strip().splitlines()

    start=[list(map(int,lines[0].split())),
           list(map(int,lines[1].split())),
           list(map(int,lines[2].split()))]
        
    goal=[list(map(int,lines[3].split())),
          list(map(int,lines[4].split())),
          list(map(int,lines[5].split()))]
        

    x=y=0
    for i in range(3):
        for j in range(3):
            if start[i][j]==0:
                x,y=i,j


    with open("output_bfs.txt","w") as out:
        out.write("bfs soln\n")
        bfs(start,goal,x,y,out)