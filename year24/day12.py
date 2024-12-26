
from aoclib import *
from queue import Queue

fs = [
    'ex12c.txt',
    'ex12b.txt',
    'ex12d.txt',
    'in12.txt'
]
#lines = parse_input("in12.txt")
#lines = parse_input("ex12a.txt")
lines = parse_input(fs[-1])

g = PlotGrid(lines)


def p1():
    regions = []
    seen = set()
    # find all regions
    # loop over all nodes
    for r in range(g.R):
        for c in range(g.C):
            v = g.at(r,c)
            n = Node(r,c,v)
            if n not in seen:
                ns = g.bfs_get_rnodes(Node(r,c,g.at(r,c)))
                regions.append(ns)
                seen |= ns
                seen.add(n)

    ans = 0
    # ok, we got each region
    for region in regions:
        area = len(region)
        perim = 0
        nn = Node(1,1,1)
        for n in region:
            nbrs = g.get_nbrs(n.r,n.c)
            same_nbrs = [nbr for nbr in nbrs if nbr.v == n.v]
            perim += 4 - len(same_nbrs)
            nv = n.v
        price = area*perim
        #print(f"- A region of {nv} plants with price {area:2d} * {perim:2d} = {price:3d}")
        ans += price

    print(f"[p1] total price: {ans:7d}")

def p2():

    regions = []
    seen = set()
    # find all regions
    # loop over all nodes
    for r in range(g.R):
        for c in range(g.C):
            v = g.at(r,c)
            n = Node(r,c,v)
            if n not in seen:
                ns = g.bfs_get_rnodes(Node(r,c,g.at(r,c)))
                regions.append(ns)
                seen |= ns
                seen.add(n)

    ans = 0


    # ok, we got each region
    for region in regions:
        area = len(region)

        n_sides = 0
        seen = set() #  ('N',r0,c0), ('N', r1,c1)...

        for n in region:

            nv = n.v
            dirs = [Dir.N, Dir.S, Dir.E, Dir.W]

            for idir in dirs:
                inbr = g.get_nbr_in_dir(n, idir)
                if inbr.v != n.v:
                    checking_node = (idir, n.r, n.c)
                    if checking_node not in seen:
                        ns = g.bfs_get_snodes(n, idir)
                        side = set([(idir, nn.r, nn.c) for nn in ns])
                        n_sides += 1
                        seen |= side
                        seen.add(checking_node)

        price = area*n_sides
        #print(f"- A region of {nv} plants with price {area:2d} * {n_sides:2d} = {price:3d}")
        ans += price

    print(f"[p2] total price: {ans:7d}")


p1()
p2()




