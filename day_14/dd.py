import sys
import math
from copy import deepcopy
from collections import defaultdict, deque
infile = 'example.txt'
infile = 'real.txt'
#infile = sys.argv[1] if len(sys.argv) > 1 else '14.in'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

R = set()
for line in lines:
    prev = None
    for point in line.split('->'):
        x,y = point.split(',')
        x,y = int(x), int(y)
        if prev is not None:
            dx = x - prev[0]
            dy = y - prev[1]
            len_ = max(abs(dx), abs(dy))
            for i in range(len_+1):
                xx = prev[0]+i*(1 if dx>0 else (-1 if dx<0 else 0 ))
                yy = prev[1]+i*(1 if dy>0 else (-1 if dy<0 else 0 ))
                R.add((xx,yy))
        prev = (x,y)

floor = max([r[1] for r in R])
floor += 2
for x in range(-10000,10000):
    R.add((x,floor))

for t in range(1000000):
    rock = (500, 0)
    while True:
        #if rock[1] > floor:
            #assert False, t
        #if rock[1] >= floor:
        #    break
        if (rock[0], rock[1]+1) not in R:
            rock = (rock[0], rock[1]+1)
        elif (rock[0]-1, rock[1]+1) not in R:
            rock = (rock[0]-1, rock[1]+1)
        elif (rock[0]+1, rock[1]+1) not in R:
            rock = (rock[0]+1, rock[1]+1)
        else:
            break
    if rock == (500,0):
        assert False, t+1
    R.add(rock)

'''
'''