from typing import Tuple, List, Dict
from functools import cache


def get_load(G: Dict[tuple[int,int], str]) -> int:
    load = 0
    for k,v in G.items():
        if v == "O":
            r = k[0]
            load += R - r
    return load

def get_grid(lines: List[str]) -> Dict[tuple[int,int], str]:
    G = {}
    for r,row in enumerate(lines):
        for c,char in enumerate(row):
            G[(r,c)] = char
    return G

def print_grid(G: Dict[tuple[int,int], str], R: int, C: int) -> Dict[tuple[int,int],str]:

    for r in range(R):
        for c in range(C):
            print(G[(r,c)],end="")
        print()


def shift_n(G: Dict[tuple[int,int], str], R: int, C: int) -> Dict[tuple[int,int],str]:

    changes = True
    while changes:
        changes = False
        for k,v in G.items():
            if v == "O":
                ri,ci = k
                if ri-1 >= 0 and G[(ri-1, ci)] == ".":
                        G[(ri  ,ci)] = "."
                        G[(ri-1,ci)] = 'O'
                        changes = True
    return G

def shift_s(G: Dict[tuple[int,int], str], R: int, C: int) -> Dict[tuple[int,int],str]:

    changes = True
    while changes:
        changes = False
        for k,v in G.items():
            if v == "O":
                ri,ci = k
                if ri+1 < R and G[(ri+1, ci)] == ".":
                        G[(ri  ,ci)] = "."
                        G[(ri+1,ci)] = 'O'
                        changes = True
    return G

def shift_w(G: Dict[tuple[int,int], str], R: int, C: int) -> Dict[tuple[int,int],str]:

    changes = True
    while changes:
        changes = False
        for k,v in G.items():
            if v == "O":
                ri,ci = k
                if ci-1 >= 0 and G[(ri, ci-1)] == ".":
                        G[(ri  ,ci)] = "."
                        G[(ri,ci-1)] = 'O'
                        changes = True
    return G

def shift_e(G: Dict[tuple[int,int], str], R: int, C: int) -> Dict[tuple[int,int],str]:

    changes = True
    while changes:
        changes = False
        for k,v in G.items():
            if v == "O":
                ri,ci = k
                if ci+1 < C and G[(ri, ci+1)] == ".":
                        G[(ri  ,ci)] = "."
                        G[(ri,ci+1)] = 'O'
                        changes = True
    return G

@cache
def cycle_1(G, R, C):
    G = shift_n(G, R, C)
    G = shift_w(G, R, C)
    G = shift_s(G, R, C)
    G = shift_e(G, R, C)
    return G

    
#lstr = open("ex_post.txt").read()
#lstr = open("ex.txt").read()
lstr = open("in.txt").read()
lines = lstr.splitlines()

R = len(lines)
C = len(lines[0])
G = get_grid(lines)

def part_1(G, R, C):

    G = shift_n(G, R, C)
    
    load = get_load(G)
    print(f"load: {load}")

#N = 1000000000
#for i in range(N):
#    #print(f"After {i+1} cycles:")
#    G = cycle_1(G, R, C)
#    #print_grid(G, R, C)



