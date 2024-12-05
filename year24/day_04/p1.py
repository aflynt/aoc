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
        return f"({self.r:2d},{self.c:2d}, {self.v})"

def get_node_nbrs(G, cn: Node) -> list[Node]:
    R   = len(G)
    C   = len(G[0])
    r = cn.r
    c = cn.c
    v = cn.v
    nbrs = []
    # look east



    # try to add N
    if 0 <= r-1 < R and 0 <= c   < C : 
        nbrs.append(Node(r-1, c  , G[r-1][c])) 

    # try to add south
    if 0 <= r+1 < R and 0 <= c   < C :
        nbrs.append(Node(r+1, c  , G[r+1][c])) 

    # try to add east
    if 0 <= r   < R and 0 <= c+1 < C :
        nbrs.append(Node(r  , c+1, G[r][c+1])) 

    # try to add west
    if 0 <= r   < R and 0 <= c-1 < C :
        nbrs.append(Node( r, c-1, G[r][c-1])) 

    # try to add NE
    if 0 <= r-1   < R and 0 <= c+1 < C :
        nbrs.append(Node( r-1, c+1, G[r-1][c+1])) 

    # NW = - -
    if 0 <= r-1   < R and 0 <= c-1 < C :
        nbrs.append(Node( r-1, c-1, G[r-1][c-1])) 

    # SW = + -
    if 0 <= r+1   < R and 0 <= c-1 < C :
        nbrs.append(Node( r+1, c-1, G[r+1][c-1])) 

    # SE = + +
    if 0 <= r+1   < R and 0 <= c+1 < C :
        nbrs.append(Node( r+1, c+1, G[r+1][c+1])) 

    return nbrs

def print_nums(mem):
    # print a list of numbers 
    for i in range(0,80):
        if i%10 == 0:
            pstr = "_"
        else:
            pstr = f"{i%10:d}"
        print(pstr, end="")
    print()

def get_input(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

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

fname = "ex.txt"

G = get_grid(fname)


def get_xnodes(G):
    xnodes = []
    R = len(G)
    C = len(G[0])

    pstr = "."
    for r in range(R):
        for c in range(C):
            n = Node(r,c, G[r][c])
            if n.v == "X":
                nbrs = get_node_nbrs(G, n)
                mnbrs = [n for n in nbrs if n.v == "M"]

                MEs = [n for n in mnbrs if n.r == r and n.c == c+1]
                MWs = [n for n in mnbrs if n.r == r and n.c == c-1]
                MNs = [n for n in mnbrs if n.r == r-1 and n.c == c]
                MSs = [n for n in mnbrs if n.r == r+1 and n.c == c]
                MSEs = [n for n in mnbrs if n.r == r+1 == n.c == c+1]
                MSWs = [n for n in mnbrs if n.r == r+1 == n.c == c-1]
                MNWs = [n for n in mnbrs if n.r == r-1 == n.c == c-1]
                MNEs = [n for n in mnbrs if n.r == r-1 == n.c == c+1]

                print(f"X: {n}")
                print(f"  - MEs : {MEs }")
                print(f"  - MWs : {MWs }")
                print(f"  - MNs : {MNs }")
                print(f"  - MSs : {MSs }")
                print(f"  - MSEs: {MSEs}")
                print(f"  - MSWs: {MSWs}")
                print(f"  - MNWs: {MNWs}")
                print(f"  - MNEs: {MNEs}")



get_xnodes(G)

print_grid(G)