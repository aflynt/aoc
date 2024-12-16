import aoclib as xl
from aoclib import Grid, Node

def get_nbrs(g: Grid, v: Node):
    nbrs = set()
    drcs = [
       (-1,  0),
       ( 1,  0),
       ( 0,  1),
       ( 0, -1),
    ]
    for drc in drcs:
        dr,dc = drc
        rr,cc = v.r + dr, v.c + dc
        if 0 <= rr < g.R and 0 <= cc < g.C:
            nbr_v = g.G[rr][cc]
            if nbr_v - v.v == 1:
                nbrs.add(xl.Node(rr,cc,nbr_v))
    return nbrs


def dfsa(g: Grid, v: Node):
    # label v as discovered
    nbr9s = set()
    seen = set()
    seen.add(v)
    if v.v == 9:
        nbr9s.add(Node(v.r, v.c, v.v))
        return nbr9s
    else:
        # get neighbors
        nbrs = get_nbrs(g, v)
        for nbr in nbrs:
            if nbr not in seen:
                nbr9s |= dfsa(g, nbr)
    return nbr9s

def dfsb(g: Grid, v: Node):
    # label v as discovered
    nbr9s = []
    seen = set()
    seen.add(v)
    if v.v == 9:
        nbr9s.append(Node(v.r, v.c, v.v))
        return nbr9s
    else:
        # get neighbors
        nbrs = get_nbrs(g, v)
        for nbr in nbrs:
            if nbr not in seen:
                nbr9s += dfsb(g, nbr)
    return nbr9s
# ------------------------------------------
def fp1(ths, g):
    p1 = 0
    for th in ths:
        nbr9s = dfsa(g, th)
        N = len(nbr9s)
        #print(f"TH: {th} -> N: {N} from {nbr9s}")
        p1 += N
    print(f" ans = {p1}")

def fp2(ths, g):
    p2 = 0
    for th in ths:
        nbr9s = dfsb(g, th)
        N = len(nbr9s)
        #print(f"TH: {th} -> N: {N} from {nbr9s}")
        p2 += N
    print(f" ans = {p2}")

def main():
    #lines = xl.parse_input("ex10.txt")
    #lines = xl.parse_input("ex10a.txt")
    #lines = xl.parse_input("ex10b.txt")
    lines = xl.parse_input("in10.txt")
    lines = [l for l in lines if len(l) > 1]
    
    g = Grid(lines)
    ths = g.get_trailheads()
    
    fp1(ths, g)
    fp2(ths, g)


if __name__ == "__main__":
    main()