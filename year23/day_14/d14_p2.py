from typing import Tuple, List, Dict
from functools import cache

#lstr = open("ex.txt").read()
lstr = open("in.txt").read()
lines = lstr.splitlines()

R = len(lines)
C = len(lines[0])

def get_balls(lines):
    bs = []
    for r,row in enumerate(lines):
        for c,char in enumerate(row):
            if char == "O":
                bs.append((r,c))
    bs = tuple(sorted(bs))
    return bs

def get_walls(lines):

    walls = set()
    for r,row in enumerate(lines):
        for c,char in enumerate(row):
            if char == "#":
                walls.add((r,c))
    return walls
                
bs = get_balls(lines)
ws = get_walls(lines)



def get_ball_load(brs: list[int]) -> int:
    load = 0
    for r in brs:
        load += R - r
    return load

def get_list(bs ):
    return list(bs)

def get_tuple(bs):
    return tuple(sorted(bs))

def is_free_of_bs(r,c, bs):
    return (r,c) not in bs

def is_free_of_ws(r,c, ws):
    return (r,c) not in ws

#@cache

#xbs = {}
def shift_balls_x(bs: tuple[tuple[int,int]], dr: int, dc: int) -> tuple[tuple[int,int]]:
    #if bs in xbs:
    #    return xbs[bs]
    bs = list(bs)

    changes = True
    while changes:
        changes = False
        for i,rc in enumerate(bs):
            r,c = rc
            rn = r+dr
            cn = c+dc
            if 0 <= rn < R and 0 <= cn < C:
                is_free_from_bs = is_free_of_bs(rn,cn, bs)
                is_free_from_ws = is_free_of_ws(rn,cn, ws)
                is_free = is_free_from_ws and is_free_from_bs
                if is_free:
                    bs[i] = (rn,cn)
                    changes = True

    bs = tuple(sorted(bs))
    #xbs[bs] = bs
    return bs

#@cache
def cycle_1(bs: tuple[tuple[int,int]]) -> tuple[tuple[int,int]]:

    bs = shift_balls_x(bs, -1,  0) # N
    bs = shift_balls_x(bs,  0, -1) # W
    bs = shift_balls_x(bs,  1,  0) # S
    bs = shift_balls_x(bs,  0,  1) # E

    return bs

def part_1(bs):

    bs = shift_balls_x(bs, -1, 0)
    
    brs = [r for r,_ in bs]
    load = get_ball_load(brs)
    print(f"load: {load}")

def print_platform(bs: tuple[tuple[int,int]] ) -> None:

    for r in range(R):
        for c in range(C):
            if (r,c) in bs:
                char = "O"
            elif (r,c) in ws:
                char = "#"
            else:
                char = "."
            print(char,end="")
        print()

    
#########################################
#part_1(bs)
#print_platform(bs)
#print(f"--------------------------")

print(f"NR = {R}")
print(f"NC = {C}")

#N = 1000000000
#N = 3
N = 200
TEN_MILS = 0
for i in range(N):
    #print(f"After {i+1} cycles:")
    #print(".",end="")
    #if TEN_MILS > 80:
    #    TEN_MILS = 0
    #    print()
    #if i % 1e7 == 0:
    #    TEN_MILS += 1
    #    print(TEN_MILS)
    bs = cycle_1(bs)
    brs = [r for r,_ in bs]
    load = get_ball_load(brs)
    print(f"{i+1:2d} load: {load}")
    #print_platform(bs)
    TEN_MILS += 1



"""
"""