from queue import Queue
from enum import Enum

class Dir(Enum):
    N = 0
    S = 1
    E = 2
    W = 3


class Node:
    def __init__(self, r,c,v):
        self.r = r
        self.c = c
        self.v = v
    def __str__(self) -> str:
        return f"N({self.r},{self.c},{self.v})"
    def __repr__(self) -> str:
        return f"N({self.r},{self.c},{self.v})"
    def __hash__(self):
        return hash((self.r, self.c, self.v))
    def __lt__(self, other):
        return (self.r, self.c) < (other.r, other.c)
    def __eq__(self, other):
        return (self.r, self.c) == (other.r, other.c)

class PlotGrid:
    def __init__(self, lines):
        self.R = len(lines)
        self.C = len(lines[0])
        self.G = [[line[c] for c in range(self.C)] for line in lines]
    def at(self, r,c):
        if 0 <= r < self.R and 0 <= c < self.C:
            return self.G[r][c]
        return '_'
    def prn(self):
        for r in range(self.R):
            for c in range(self.C):
                print(self.G[r][c],end=' ')
            print()
    def get_plot_types(self):
        plot_types = set()
        for r in range(self.R):
            for c in range(self.C):
                plot_types.add(self.at(r,c))
        return plot_types
    def rc_ok(self, r,c):
        if 0 <= r < self.R and 0 <= c < self.C:
            return True
        return False

    def get_nbrs(self, r,c):

        nbrs = []

        drcs = [(-1,0),(1,0),(0,-1),(0,1)]
        for drc in drcs:
            dr,dc = drc
            rr = r + dr
            cc = c + dc
            if self.rc_ok(rr,cc):
                nbrs.append(Node(rr,cc,self.G[rr][cc]))
        return nbrs
    
    def get_nbr_in_dir(self, n: Node, dir: Dir):
        r = n.r
        c = n.c

        if self.has_nbr_in_dir(n, dir):

            match dir:
                case Dir.N: return Node(r-1, c, self.at(r-1, c))
                case Dir.S: return Node(r+1, c, self.at(r+1, c))
                case Dir.E: return Node(r, c+1, self.at(r, c+1))
                case Dir.W: return Node(r, c-1, self.at(r, c-1))
                case _:     return Node(-1,-1,"_")
        else:
            return Node(-1,-1,"_")

    def has_nbr_in_dir(self, n: Node, dir: Dir):
        r = n.r
        c = n.c
        match dir:
            case Dir.N: return self.rc_ok(r-1, c)
            case Dir.S: return self.rc_ok(r+1, c)
            case Dir.E: return self.rc_ok(r, c+1)
            case Dir.W: return self.rc_ok(r, c-1)
            case _:     return False
        return False
            
    def bfs_get_snodes(self, n: Node, dir: Dir):
        visited = set()
        q = Queue()

        visited.add(n)
        q.put(n)

        ns = set()
        ns.add(n)
        
        while not q.empty():
            m = q.get()
            r = m.r
            c = m.c
            visited.add(m)

            # get LNBR, RNBR
            match dir:
                case Dir.N: 
                    lnbr   = Node(r, c-1, self.at(r, c-1))
                    rnbr   = Node(r, c+1, self.at(r, c+1))
                    lnbr_s = Node(r-1, c-1, self.at(r-1, c-1))
                    rnbr_s = Node(r-1, c+1, self.at(r-1, c+1))
                case Dir.S: 
                    lnbr   = Node(r, c-1, self.at(r, c-1))
                    rnbr   = Node(r, c+1, self.at(r, c+1))
                    lnbr_s = Node(r+1, c-1, self.at(r+1, c-1))
                    rnbr_s = Node(r+1, c+1, self.at(r+1, c+1))
                case Dir.E: 
                    lnbr   = Node(r+1, c, self.at(r+1, c))
                    rnbr   = Node(r-1, c, self.at(r-1, c))
                    lnbr_s = Node(r+1, c+1, self.at(r+1, c+1))
                    rnbr_s = Node(r-1, c+1, self.at(r-1, c+1))
                case Dir.W: 
                    lnbr   = Node(r+1, c, self.at(r+1, c))
                    rnbr   = Node(r-1, c, self.at(r-1, c))
                    lnbr_s = Node(r+1, c-1, self.at(r+1, c-1))
                    rnbr_s = Node(r-1, c-1, self.at(r-1, c-1))

            if lnbr.v == n.v and lnbr_s.v != n.v and lnbr not in visited:
                q.put(lnbr)
                ns.add(lnbr)

            if rnbr.v == n.v and rnbr_s.v != n.v and rnbr not in visited:
                q.put(rnbr)
                ns.add(rnbr)
        return ns

                



        

    def bfs_get_rnodes(self, n: Node):
        visited = set()
        q = Queue()

        visited.add(n)
        q.put(n)

        ns = set()
        ns.add(n)

        while not q.empty():
            m = q.get()
            nbrs = self.get_nbrs(m.r,m.c)
            for nbr in nbrs:
                if nbr not in visited:
                    visited.add(nbr)
                    if nbr.v == n.v:
                        ns.add(nbr)
                        q.put(nbr)

        return ns

    def find_regions(self):
        region_sets = []
        region = set()
        seen = set()
        for r in range(self.R):
            for c in range(self.C):
                pass


class Grid:
    def __init__(self, lines):
        self.R = len(lines)
        self.C = len(lines[0])
        self.G = [[int(line[c]) for c in range(self.C)] for line in lines]
        self.visited = set()

    def prn(self):
        for r in range(self.R):
            for c in range(self.C):
                print(self.G[r][c],end=' ')
            print()

    def add_char(self, loc_rc, char="*"):
        r,c = loc_rc
        self.G[r][c] = char

    def rm_char(self, loc_rc, char="*"):
        r,c = loc_rc
        if self.G[r][c] == char:
            self.G[r][c] = "."

    def get_trailheads(self):
        ths = set()
        # trailheads start at zero
        for r in range(self.R):
            for c in range(self.C):
                if self.G[r][c] == 0:
                    ths.add(Node(r,c,0))
        return ths



class Antenna:
    def __init__(self, r,c,v):
        self.r = r
        self.c = c
        self.v = v
    def __str__(self) -> str:
        return f"A({self.r},{self.c},{self.v})"
    def __repr__(self) -> str:
        return f"A({self.r},{self.c},{self.v})"
    def __hash__(self):
        return hash((self.r, self.c, self.v))

class Antinode:
    def __init__(self, r,c):
        self.r = r
        self.c = c
    def __str__(self) -> str:
        return f"a({self.r},{self.c})"
    def __repr__(self) -> str:
        return f"a({self.r},{self.c})"
    def __hash__(self):
        return hash((self.r, self.c))



def parse_input(fname):

    d = open(fname, "r").read()
    lines = d.split("\n")

    return lines
