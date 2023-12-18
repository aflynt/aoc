from enum import Enum
import sys
import math as m

class Dir(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name

def get_grid(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    rows = [line.strip("\n") for line in lines]
    G = [[int(c) for c in r] for r in rows]

    return G

def print_grid(G):
    R = len(G)
    C = len(G[0])
    for r in range(R):
        nums = [str(G[r][c]) for c in range(C)]
        print("".join(nums))

def pick_mv():
    x = input("dir: (0N, 1S, 2E, 3W)")
    return int(x)

def get_nbrs(G, pos: tuple[int,int,int,int,Dir]) -> list[tuple[int,int,int,int,Dir]]:
    R   = len(G)
    C   = len(G[0])
    f   = pos[0]
    r   = pos[1]
    c   = pos[2]
    mvs = pos[3]
    dir = pos[4]
    nbrs = []
    if dir == Dir.E:
        if 0 <= r-1 < R and 0 <= c   < C:
            nbrs.append((0, r-1, c, 1, Dir.N)) 
        if 0 <= r+1 < R and 0 <= c   < C:
            nbrs.append((0, r+1, c, 1, Dir.S)) 
        if 0 <= r   < R and 0 <= c+1 < C and mvs < 3:
            nbrs.append((0, r, c+1, mvs+1, Dir.E)) 
    elif dir == Dir.W:
        if 0 <= r-1 < R and 0 <= c   < C:
            nbrs.append((0, r-1, c, 1, Dir.N)) 
        if 0 <= r+1 < R and 0 <= c   < C:
            nbrs.append((0, r+1, c, 1, Dir.S)) 
        if 0 <= r   < R and 0 <= c-1 < C and mvs < 3:
            nbrs.append((0, r, c-1, mvs+1, Dir.W)) 
    elif dir == Dir.N:
        if 0 <= r   < R and 0 <= c+1 < C:
            nbrs.append((0, r, c+1, 1, Dir.E)) 
        if 0 <= r   < R and 0 <= c-1 < C:
            nbrs.append((0, r, c-1, 1, Dir.W)) 
        if 0 <= r-1 < R and 0 <= c   < C and mvs < 3:
            nbrs.append((0, r-1, c, mvs+1, Dir.N)) 
    elif dir == Dir.S:
        if 0 <= r   < R and 0 <= c+1 < C:
            nbrs.append((0, r, c+1, 1, Dir.E)) 
        if 0 <= r   < R and 0 <= c-1 < C:
            nbrs.append((0, r, c-1, 1, Dir.W)) 
        if 0 <= r+1 < R and 0 <= c   < C and mvs < 3:
            nbrs.append((0, r+1, c, mvs+1, Dir.S)) 
    else:
        assert False
    return nbrs

def reconstruct_path(cameFrom: dict[tuple[int,int,int,int,Dir]], current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path

def h(node,R,C):
    # node = (f,r,c,mvs, dir)
    r = node[1]
    c = node[2]
    gr = R-1
    gc = C-1
    dx = abs(r-gr) + abs(c-gc)
    return dx


def init_gscore(start,R,C):
    gScore = {} # defaults = infinity??
    for r in range(R):
        for c in range(C):
            for mv in [1, 2, 3]:
                for dir in [Dir.N, Dir.S, Dir.E, Dir.W]:
                    gScore[(r,c,mv, dir)] = sys.maxsize
    gScore[start] = 0
    return gScore

def init_fscore(start,R,C):
    fScore = {} # defaults = infinity??
    for r in range(R):
        for c in range(C):
            for mv in [1, 2, 3]:
                for dir in [Dir.N, Dir.S, Dir.E, Dir.W]:
                    fScore[(r,c,mv, dir)] = sys.maxsize
    fScore[start] = h(start, R, C)
    return fScore