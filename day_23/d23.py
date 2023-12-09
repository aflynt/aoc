from collections import deque
from lib import *

###############################################################

dirs = deque(['N', 'S', 'W', 'E'])

def get_limits(E):
    rmin = min([r for r,c in E])
    rmax = max([r for r,c in E])
    cmin = min([c for r,c in E])
    cmax = max([c for r,c in E])
    return rmin,rmax,cmin,cmax

def new_print_grid(E:set[(int,int)]):
    rmin,rmax,cmin,cmax = get_limits(E)

    for r in range(rmin,rmax+1):
        for c in range(cmin, cmax+1):
            char = '#' if (r,c) in E else '.'
            print(char, end='')
        print()

def gather_elves(lines):
    E = set()
    for r,row in enumerate(lines):
        for c,char in enumerate(row):
            if char == '#':
                E.add((r,c))
    return E

def get_elf_moves(E:set[tuple[int,int]]):

    dst_list = []
    src_list = []


    for e in E:
        r,c = e

        # consider 8 locations around me
        loc_n  = (r-1, c  )
        loc_s  = (r+1, c  )
        loc_e  = (r  , c+1)
        loc_w  = (r  , c-1)
        loc_ne = (r-1, c+1)
        loc_se = (r+1, c+1)
        loc_nw = (r-1, c-1)
        loc_sw = (r+1, c-1)

        nbrs = [ loc_n  ,loc_s  ,loc_e  ,loc_w  ,loc_ne ,loc_se ,loc_nw ,loc_sw , ]

        nbrs = [nbr for nbr in nbrs if nbr in E]

        #print(f'({r},{c}) has nbrs = {nbrs}')

        if len(nbrs) == 0:
            continue
            #print(f'nobody around: dont move')

        mv_ok = False
        # now check the n e s w directions
        for dir in dirs:
            if dir == 'N' and (not mv_ok) and (loc_n not in E) and (loc_nw not in E) and (loc_ne not in E):
                mvTo = loc_n
                mv_ok = True
            if dir == 'E' and (not mv_ok) and (loc_e not in E) and (loc_se not in E) and (loc_ne not in E):
                mvTo = loc_e
                mv_ok = True
            if dir == 'S' and (not mv_ok) and (loc_s not in E) and (loc_se not in E) and (loc_sw not in E):
                mvTo = loc_s
                mv_ok = True
            if dir == 'W' and (not mv_ok) and (loc_w not in E) and (loc_nw not in E) and (loc_sw not in E):
                mvTo = loc_w
                mv_ok = True
        if mv_ok:
            dst_list.append(mvTo)
            src_list.append((r,c))

    map_tf = {}
        
    for to,fm in zip(dst_list, src_list):
        if to not in map_tf:
            #print(f'adding to {to} from {fm}')
            map_tf[to] = fm
        else:
            #print(f'found duplicate destination {to} coming from {fm}')
            del map_tf[to]
    
    for to,fm in map_tf.items():
        ##print(f'going TO->FM {to} -> {fm}')
        E.remove(fm)
        E.add(to)

    dirs.rotate(-1)

    return len(map_tf)

###############################################################


#fname = 'ex.dat'
#fname = 'ex2.dat'
fname = 'real.dat'

lines = read_file(fname)
E = gather_elves(lines)


#for round in range(1,10+1):
round = 1
while True:
    print(f'=============================== ROUND: {round}')
    moves = get_elf_moves(E)
    new_print_grid(E)
    if moves == 0:
        break
    round += 1


rmin,rmax,cmin,cmax = get_limits(E)

num_empty = 0

for r in range(rmin,rmax+1):
    for c in range(cmin, cmax+1):
        val = 0 if (r,c) in E else 1
        num_empty += val

print(f'num_empty = {num_empty}')
        