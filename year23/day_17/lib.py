from enum import Enum
import sys
import math as m

class Dir(Enum):
    N = 0
    S = 1
    E = 2
    W = 3
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name
    def __lt__(self, o):
        return self.value < o.value

class Node:
    def __init__(self, r, c, mvs, dir):
        self.r = r
        self.c = c
        self.mvs = mvs
        self.dir = dir
    def __lt__(self, o):
        r = self.r
        c = self.c
        m = self.mvs
        d = self.dir
        _r = o.r
        _c = o.c
        _m = o.mvs
        _d = o.dir
        return ((r,c,m,d) < ((_r,_c,_m,_d)))
    def __gt__(self, o):
        r = self.r
        c = self.c
        m = self.mvs
        d = self.dir
        _r = o.r
        _c = o.c
        _m = o.mvs
        _d = o.dir
        return ((r,c,m,d) > ((_r,_c,_m,_d)))
    def __le__(self, o):
        r = self.r
        c = self.c
        m = self.mvs
        d = self.dir
        _r = o.r
        _c = o.c
        _m = o.mvs
        _d = o.dir
        return ((r,c,m,d) <= ((_r,_c,_m,_d)))
    def __ge__(self, o):
        r = self.r
        c = self.c
        m = self.mvs
        d = self.dir
        _r = o.r
        _c = o.c
        _m = o.mvs
        _d = o.dir
        return ((r,c,m,d) >= ((_r,_c,_m,_d)))
    def __eq__(self, o):
        r = self.r
        c = self.c
        m = self.mvs
        d = self.dir
        _r = o.r
        _c = o.c
        _m = o.mvs
        _d = o.dir
        return ((r,c,m,d) == ((_r,_c,_m,_d)))
    def __hash__(self) -> int:
        r = self.r
        c = self.c
        m = self.mvs
        d = self.dir
        return hash((r,c,m,d))
    def __repr__(self) -> str:
        return f"Node({self.r},{self.c},{self.mvs},{self.dir})"
    def __str__(self) -> str:
        return f"({self.r},{self.c},{self.mvs},{self.dir})"

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

def get_node_nbrs_min_max(G, cn: Node, dmin=4, dmax=10) -> list[Node]:
    R   = len(G)
    C   = len(G[0])
    r = cn.r
    c = cn.c
    mvs = cn.mvs
    dir = cn.dir
    nbrs = []
    if dir == Dir.E:
        if 0 <= r-1 < R and 0 <= c   < C and mvs >= dmin:
            nbrs.append(Node(r-1, c  , 1, Dir.N)) 
        if 0 <= r+1 < R and 0 <= c   < C and mvs >= dmin:
            nbrs.append(Node(r+1, c  , 1, Dir.S)) 
        if 0 <= r   < R and 0 <= c+1 < C and mvs < dmax:
            nbrs.append(Node(r  , c+1, mvs+1, Dir.E)) 
    elif dir == Dir.W:
        if 0 <= r-1 < R and 0 <= c   < C and mvs >= dmin:
            nbrs.append(Node( r-1, c, 1, Dir.N)) 
        if 0 <= r+1 < R and 0 <= c   < C and mvs >= dmin:
            nbrs.append(Node( r+1, c, 1, Dir.S)) 
        if 0 <= r   < R and 0 <= c-1 < C and mvs < dmax:
            nbrs.append(Node( r, c-1, mvs+1, Dir.W)) 
    elif dir == Dir.N:
        if 0 <= r   < R and 0 <= c+1 < C and mvs >= dmin:
            nbrs.append(Node( r, c+1, 1, Dir.E)) 
        if 0 <= r   < R and 0 <= c-1 < C and mvs >= dmin:
            nbrs.append(Node( r, c-1, 1, Dir.W)) 
        if 0 <= r-1 < R and 0 <= c   < C and mvs < dmax:
            nbrs.append(Node( r-1, c, mvs+1, Dir.N)) 
    elif dir == Dir.S:
        if 0 <= r   < R and 0 <= c+1 < C and mvs >= dmin:
            nbrs.append(Node( r, c+1, 1, Dir.E)) 
        if 0 <= r   < R and 0 <= c-1 < C and mvs >= dmin:
            nbrs.append(Node( r, c-1, 1, Dir.W)) 
        if 0 <= r+1 < R and 0 <= c   < C and mvs < dmax:
            nbrs.append(Node( r+1, c, mvs+1, Dir.S)) 
    else:
        assert False
    return nbrs

def reconstruct_path(cameFrom: dict[Node], current: Node):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path

def h(node: Node, goal: Node):
    # node = (f,r,c,mvs, dir)
    r = node.r
    c = node.c
    gr = goal.r
    gc = goal.c
    dx = abs(r-gr) + abs(c-gc)
    return dx


def init_gscore(R,C, nfwd=3):
    gScore = {} # defaults = infinity??
    for r in range(R):
        for c in range(C):
            for mv in range(1,nfwd+1):
                for dir in [Dir.N, Dir.S, Dir.E, Dir.W]:
                    n = Node(r,c,mv,dir)
                    gScore[n] = sys.maxsize
    return gScore

def init_fscore(R,C, nfwd=3):
    fScore = {} # defaults = infinity??
    for r in range(R):
        for c in range(C):
            for mv in range(1,nfwd+1):
                for dir in [Dir.N, Dir.S, Dir.E, Dir.W]:
                    n = Node(r,c,mv,dir)
                    fScore[n] = sys.maxsize
    return fScore

def d(nbr: Node, G):
    # weight of edge from current to neighbor
    # cost is just cost of entering this node
    val = G[nbr.r][nbr.c]
    return val