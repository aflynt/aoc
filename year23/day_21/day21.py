from lib import *
from queue import Queue
from functools import cache

################################################

fname = ["in.txt","ex.txt"][-1]
lines = get_input(fname)
G = Grid(get_grid(lines))
sr, sc = get_start(G)
#           tile_r, tile_c, start_r, start_c
v0 = (0,0,sr,sc)
plts_nxt = set()
plts_nxt.add(v0)

###############################################
    

#def get_plots(r:int , c:int, G:Grid):

def get_plots(r:int , c:int):
    plots = set()
    deltas = [(1, 0), (-1, 0), (0, 1), (0,-1)]
    for dr,dc in deltas:
        if G.at((r+dr) % G.R, (c+dc) % G.C) != "#":
            tr, tc = get_rc_tiles(r+dr,c+dc, G.R, G.C)
            plots.add((tr, tc, (r+dr), (c+dc)))
    return plots
    
def shift_far_pts(itr, itc, far_plts, R, C):

    plts = set()
    #plts = []
    for ftr, ftc, fr, fc in far_plts:
        tr = itr + ftr
        tc = itc + ftc
        plts.add((tr,tc, fr+itr*R,fc+itc*C))
        #plts.append((tr,tc, fr+itr*R,fc+itc*C))
    #plts = sorted(plts)
    return plts


far_plt_dict = {}

def add_reachable_plots(frfcs):

    for fr, fc in frfcs:
        if (fr,fc) not in far_plt_dict:
            far_plt_dict[(fr,fc)] = get_plots(fr, fc) # check its reachable plots


NMAX = [6, 10, 50, 100, 500, 1000, 5000]
#NMAX = [6, 10, 50, 100]
for i in range(max(NMAX)):
    plts_now = plts_nxt
    plts_nxt = set()

    frfcs = set()
    for plt in plts_now:
        _, _, r, c = plt
        frfcs.add((r%G.R,c%G.C))
    
    frfc_new = {frfc for frfc in frfcs if frfc not in far_plt_dict}

    
    add_reachable_plots(frfcs)
    #for fr, fc in frfcs:
    #    add_reachable_plots
    #    far_plts = get_plots(fr, fc) # check its reachable plots
    #    far_plt_dict[(fr,fc)] = far_plts

    for plt in plts_now:
        # refind my results
        tr, tc, r, c = plt

        fr = r % G.R
        fc = c % G.C
        far_plts = far_plt_dict[(fr,fc)]
        far_plts = shift_far_pts(tr,tc, far_plts, G.R, G.C)
        plts_nxt |= far_plts
    
    #for plt in plts_now:
    #    tr, tc, r, c = plt

    #    fr = r % G.R
    #    fc = c % G.C
    #    far_plts = get_plots(fr, fc) # check its reachable plots
    #    far_plts = shift_far_pts(tr,tc, far_plts, G.R, G.C)

    #    #near_plts = get_plots(r, c, G) # check its reachable plots
    #    #near_plts_view = sorted(list(near_plts))
    #    #assert far_plts == near_plts_view
    #    #print(f"faar_plts = {far_plts}")
    #    #print(f"near_plts = {near_plts_view}")
    #    #plts_nxt |= near_plts
    #    plts_nxt |= far_plts

    if i+1 in NMAX:
        print(f"step: {i+1:2d} n_plots: {len(plts_nxt)}")
    #x = input()
    #G.print_elf_grid(elf_locs)
