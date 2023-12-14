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


@cache
def shift_balls_n(bs: tuple[tuple[int,int]]) -> tuple[tuple[int,int]]:
    bs = list(bs)

    changes = True
    while changes:
        changes = False
        for i,rc in enumerate(bs):
            r,c = rc
            rup = r-1
            if rup >= 0:
                # if free space above
                if (rup,c) not in bs and (rup,c) not in ws:
                    # move ball up
                    bs[i] = (rup,c)
                    changes = True
    bs = tuple(sorted(bs))
    return bs

@cache
def shift_balls_s(bs: tuple[tuple[int,int]]) -> tuple[tuple[int,int]]:
    bs = list(bs)

    changes = True
    while changes:
        changes = False
        for i,rc in enumerate(bs):
            r,c = rc
            rn = r+1
            if rn < R:
                # if free space above
                if (rn,c) not in bs and (rn,c) not in ws:
                    # move ball up
                    bs[i] = (rn,c)
                    changes = True
    bs = tuple(sorted(bs))
    return bs

@cache
def shift_balls_w(bs: tuple[tuple[int,int]]) -> tuple[tuple[int,int]]:
    bs = list(bs)

    changes = True
    while changes:
        changes = False
        for i,rc in enumerate(bs):
            r,c = rc
            cn = c-1
            if cn >= 0:
                # if free space above
                if (r,cn) not in bs and (r,cn) not in ws:
                    # move ball west
                    bs[i] = (r,cn)
                    changes = True
    bs = tuple(sorted(bs))
    return bs

@cache
def shift_balls_e(bs: tuple[tuple[int,int]]) -> tuple[tuple[int,int]]:
    bs = list(bs)

    changes = True
    while changes:
        changes = False
        for i,rc in enumerate(bs):
            r,c = rc
            cn = c+1
            if cn < C:
                # if free space above
                if (r,cn) not in bs and (r,cn) not in ws:
                    # move ball west
                    bs[i] = (r,cn)
                    changes = True

    bs = tuple(sorted(bs))
    return bs


@cache
def cycle_1(bs: tuple[tuple[int,int]]) -> tuple[tuple[int,int]]:

    bs = shift_balls_n(bs)
    bs = shift_balls_w(bs)
    bs = shift_balls_s(bs)
    bs = shift_balls_e(bs)

    return bs

def part_1(bs):

    bs = shift_balls_n(bs)
    
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

N = 1000000000
TEN_MILS = 0
for i in range(N):
    #print(f"After {i+1} cycles:")
    if i % 1e7 == 0:
        TEN_MILS += 1
        print(TEN_MILS)
    bs = cycle_1(bs)
    #print_platform(bs)

brs = [r for r,_ in bs]
load = get_ball_load(brs)
print(f"load: {load}")
#

