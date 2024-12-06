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

dirs = [
    Dir.E,
    Dir.W,
    Dir.N,
    Dir.S,
    Dir.SE,
    Dir.SW,
    Dir.NW,
    Dir.NE,
]

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

def get_nbrs_matching_char(G, cn: Node, c: str):

    mnbrs = []
    for d in dirs:
        nbr = get_nbr(G, cn, d)
        if nbr and nbr.v == c:
            mnbrs.append((d,nbr))
    return mnbrs


def get_nbr(G, cn: Node, dir: Dir):

    R   = len(G)
    C   = len(G[0])
    r = cn.r
    c = cn.c

    match dir:
        case Dir.N:
            # try to add N
            if 0 <= r-1 < R and 0 <= c   < C : 
                return Node(r-1, c  , G[r-1][c])
        case Dir.S:
            # try to add south
            if 0 <= r+1 < R and 0 <= c   < C :
                return Node(r+1, c  , G[r+1][c])
        case Dir.E:
            # try to add east
            if 0 <= r   < R and 0 <= c+1 < C :
                return Node(r  , c+1, G[r][c+1])
        case Dir.W:
            # try to add west
            if 0 <= r   < R and 0 <= c-1 < C :
                return Node( r, c-1, G[r][c-1])
        case Dir.NE:
            # try to add NE
            if 0 <= r-1   < R and 0 <= c+1 < C :
                return Node( r-1, c+1, G[r-1][c+1])
        case Dir.NW:
            # NW = - -
            if 0 <= r-1   < R and 0 <= c-1 < C :
                return Node( r-1, c-1, G[r-1][c-1])
        case Dir.SW:
            # SW = + -
            if 0 <= r+1   < R and 0 <= c-1 < C :
                return Node( r+1, c-1, G[r+1][c-1])
        case Dir.SE:
            # SE = + +
            if 0 <= r+1   < R and 0 <= c+1 < C :
                return Node( r+1, c+1, G[r+1][c+1])
        case _:
            return None
    return None


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

#fname = "ex.txt"
fname = "in.txt"

G = get_grid(fname)



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
                           print(f" {ans:2d}: {n}->{mdir:2s} {mn}, {anbr}, {snbr}")




p1(G)

#print_grid(G)