import re
from typing import List
from itertools import accumulate
from enum import Enum

class Dir(Enum):
    N = 0
    S = 1
    E = 2
    W = 3
    NE = 4
    SE = 5
    SW = 6
    NW = 7
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name
    def __lt__(self, o):
        return self.value < o.value

dirs = [Dir.E,Dir.W,Dir.N,Dir.S,Dir.SE,Dir.SW,Dir.NW,Dir.NE,]

class Node:
    def __init__(self, r, c, v):
        self.r = r
        self.c = c
        self.v = v
    def __hash__(self)-> int:
        r = self.r
        c = self.c
        v = self.v
        return hash((r,c,v))
    def __repr__(self) -> str:
        return f"Node({self.r:2d},{self.c:2d}, {self.v})"
    def __str__(self) -> str:
        return f"({self.r:3d},{self.c:3d}, {self.v})"

def get_nbrs_matching_char(G, cn: Node, c: str):

    mnbrs = []
    for d in dirs:
        nbr = get_nbr(G, cn, d)
        if nbr and nbr.v == c:
            mnbrs.append((d,nbr))
    return mnbrs

def get_nbr(G, cn: Node, dir: Dir, bad_char="*"):

    R   = len(G)
    C   = len(G[0])
    r = cn.r
    c = cn.c
    n = Node(-1, -1, bad_char)

    match dir:
        case Dir.N:
            if 0 <= r-1 < R and 0 <= c   < C : 
                n = Node(r-1, c  , G[r-1][c])
        case Dir.S:
            if 0 <= r+1 < R and 0 <= c   < C :
                n = Node(r+1, c  , G[r+1][c])
        case Dir.E:
            if 0 <= r   < R and 0 <= c+1 < C :
                n = Node(r  , c+1, G[r][c+1])
        case Dir.W:
            if 0 <= r   < R and 0 <= c-1 < C :
                n = Node( r, c-1, G[r][c-1])
        case Dir.NE:
            if 0 <= r-1   < R and 0 <= c+1 < C :
                n = Node( r-1, c+1, G[r-1][c+1])
        case Dir.NW:
            if 0 <= r-1   < R and 0 <= c-1 < C :
                n = Node( r-1, c-1, G[r-1][c-1])
        case Dir.SW:
            if 0 <= r+1   < R and 0 <= c-1 < C :
                n = Node( r+1, c-1, G[r+1][c-1])
        case Dir.SE:
            if 0 <= r+1   < R and 0 <= c+1 < C :
                n = Node( r+1, c+1, G[r+1][c+1])
        case _:
            return n
    return n

def get_grid(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    rows = [line.strip("\n") for line in lines]
    G = [[c for c in r] for r in rows]

    return G

def print_grid(G):
    R = len(G)
    C = len(G[0])
    for r in range(R):
        nums = [str(G[r][c]) for c in range(C)]
        print("".join(nums))

def p1(G):
    ans = 0
    R = len(G)
    C = len(G[0])

    for r in range(R):
        for c in range(C):
            n = Node(r,c, G[r][c])
            if n.v == "X":
                # ok found n is an x, now look for m
                mnbrs = get_nbrs_matching_char(G, n, "M")

                for mnbr in mnbrs:
                    mdir,mn = mnbr
                    # ok i have an Mnode in the direction of mdir

                    # get A in mdir direction
                    anbr = get_nbr(G, mn, mdir)
                    if anbr and anbr.v == 'A':
                       snbr = get_nbr(G, anbr, mdir)
                       if snbr and snbr.v == 'S':
                           ans += 1
                           #print(f" {ans:2d}: {n}->{mdir:2s} {mn}, {anbr}, {snbr}")
    print(ans)

def p2(G):
    ans = 0
    R = len(G)
    C = len(G[0])


    for r in range(R):
        for c in range(C):
            n = Node(r,c, G[r][c])
            if n.v == "A":
                NE = get_nbr(G, n, Dir.NE).v
                NW = get_nbr(G, n, Dir.NW).v
                SE = get_nbr(G, n, Dir.SE).v
                SW = get_nbr(G, n, Dir.SW).v

                got_x = False
                if  NW == 'S' and NE == 'S' and SE == 'M' and SW == 'M': got_x = True
                if  NW == 'M' and NE == 'S' and SE == 'S' and SW == 'M': got_x = True
                if  NW == 'M' and NE == 'M' and SE == 'S' and SW == 'S': got_x = True
                if  NW == 'S' and NE == 'M' and SE == 'M' and SW == 'S': got_x = True

                if got_x:
                    ans += 1
                    #print(f" {ans:3d}: {n} ")
    print(ans)



#fname = "ex.txt"
fname = "in.txt"

G = get_grid(fname)


p1(G)
p2(G)

#print_grid(G)