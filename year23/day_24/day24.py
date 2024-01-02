import numpy as np
from itertools import combinations
import math as m
from z3 import *

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u,v2_u), -1.0, 1.0))

def get_input(fname):
    lines = open(fname, "r").read().strip("\n").split("\n")
    return lines

def parse_lines(lines):
    stones = []
    for line in lines:
        ps,vs = line.split(" @ ")
        px,py,pz = ps.split(",")
        vx,vy,vz = vs.split(",")

        px = int(px.strip())
        py = int(py.strip())
        pz = int(pz.strip())
        vx = int(vx.strip())
        vy = int(vy.strip())
        vz = int(vz.strip())
        
        stones.append((px,py,pz,vx,vy,vz))
    return stones

def solve_part1(stones, LIMITS):
    xlo = LIMITS[0]
    xhi = LIMITS[1]
    stone_combos = combinations(stones,2)
    
    NOK = 0
    for s0,s1 in stone_combos:
        x0,y0,vx0,vy0 = s0
        x1,y1,vx1,vy1 = s1
        m0 = vy0/vx0
        m1 = vy1/vx1
    
        Acoefs0 = [ -m0 , 1]
        Acoefs1 = [ -m1 , 1]
        bv = [ y0 - m0*x0,y1 - m1*x1]
    
        a = np.array([Acoefs0, Acoefs1])
        b = np.array(bv)
        try:
            x = np.linalg.solve(a,b)
    
            vec_fwd0 = [vx0, vy0]
            vec_fwd1 = [vx1, vy1]
            vec_to_x0 = x - np.array([x0,y0])
            vec_to_x1 = x - np.array([x1,y1])
    
            angle_0 = angle_between(vec_fwd0, vec_to_x0)
            angle_1 = angle_between(vec_fwd1, vec_to_x1)
    
            a0_ok = angle_0 < m.pi/2
            a1_ok = angle_1 < m.pi/2
    
            ge_lo = x >= xlo
            le_hi = x <= xhi
            both_in = ge_lo.all() and le_hi.all()
            both_fwd = a0_ok and a1_ok
            ok = both_fwd and both_in
            if ok:
                NOK += 1
    
        except:
            pass
    return NOK

PICK = 1
fname = ["ex.txt", "in.txt"][PICK]
LIMITS = [ (7, 27), (200000000000000,400000000000000 ),][PICK]

lines = get_input(fname)
stones = parse_lines(lines)

#NOK = solve_part1(stones, LIMITS) # 12938
#print(f"NOK: {NOK}")

def f(s):
    return Real(s)

n = len(stones)
x,y,z,vx,vy,vz = f('x'),f('y'),f('z'),f('vx'),f('vy'),f('vz')
T = [f(f'T{i}') for i in range(n)]
SOLVE = Solver()
for i in range(n):
  SOLVE.add(x + T[i]*vx - stones[i][0] - T[i]*stones[i][3] == 0)
  SOLVE.add(y + T[i]*vy - stones[i][1] - T[i]*stones[i][4] == 0)
  SOLVE.add(z + T[i]*vz - stones[i][2] - T[i]*stones[i][5] == 0)
res = SOLVE.check()
M = SOLVE.model()
print(M.eval(x+y+z))