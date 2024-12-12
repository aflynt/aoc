from enum import Enum
import time

def parse_input(fname):

    d = open(fname, "r").read()
    lines = d.split("\n")

    return lines


class Dir(Enum):
    N = 0
    S = 1
    E = 2
    W = 3
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name
    def __lt__(self, o):
        return self.value < o.value


class Grid:
    def __init__(self, lines):
        self.R = len(lines)
        self.C = len(lines[0])
        self.G = [[line[c] for c in range(self.C)] for line in lines]
        self.visited = set()

    def prn(self):
        for r in range(self.R):
            for c in range(self.C):
                rcds = [ (r,c,d) for d in [Dir.N, Dir.S, Dir.E, Dir.W]]
                rc_visited = [rcd in self.visited for rcd in rcds]
                if any(rc_visited):
                    print("*",end='')
                else:
                    print(self.G[r][c],end='')
            print()

    def add_box(self, loc_rc):
        r,c = loc_rc
        self.G[r][c] = "O"

    def rm_box(self, loc_rc):
        r,c = loc_rc
        if self.G[r][c] == "O":
            self.G[r][c] = "."


class Guard:
    def __init__(self, r, c, dir):
        self.r = r
        self.c = c
        self.dir = dir
        self.ongrid = True
        self.inloop = False

    def __str__(self) -> str:
        return f"G-({self.r}, {self.c}, {self.dir})"
    def __repr__(self) -> str:
        return f"Guard({self.r}, {self.c}, {self.dir})"
    def get_loc(self):
        return (self.r, self.c, self.dir)

    def turn(self):
        match self.dir:
            case Dir.N:  self.dir = Dir.E
            case Dir.S:  self.dir = Dir.W
            case Dir.E:  self.dir = Dir.S
            case Dir.W:  self.dir = Dir.N


    def get_new_rc(self, g: Grid):
        match self.dir:
            case Dir.N:  dr,dc = -1, 0
            case Dir.S:  dr,dc =  1, 0
            case Dir.E:  dr,dc =  0, 1
            case Dir.W:  dr,dc =  0,-1
            case _:      dr,dc =  0,-1
        nr,nc = self.r+dr, self.c+dc
        return (nr,nc)
    
    def get_char_ahead(self, g: Grid):

        nr,nc = self.get_new_rc(g)

        if nr < 0 or nc < 0 or nr >= g.R or nc >= g.C:
            return ""
        # check what is at new r,c
        nval = g.G[nr][nc]
        return nval

    def step(self, g: Grid):

        nr,nc = self.get_new_rc(g)

        # off grid -> return
        if nr < 0 or nc < 0 or nr >= g.R or nc >= g.C:
            self.ongrid = False
            return 

        # ok, nr,nc is on grid
        ca = g.G[nr][nc]
        if ca == "#" or ca == "O":
            self.turn()
            self.step(g)
        else:
            self.r = nr
            self.c = nc
            if (nr,nc,self.dir) in g.visited:
                self.inloop = True
            g.visited.add(self.get_loc())
            return 
            
def find_guard(g: Grid):
    grd = Guard(0,0,Dir.N)
    for r in range(g.R):
        for c in range(g.C):
            v = g.G[r][c]
            if v == "^":
                grd = Guard(r,c, Dir.N)
    return grd

def p1():

    #lines = parse_input("day06ex.txt")
    lines = parse_input("day06in.txt")
    g = Grid(lines)
    grd = find_guard(g)
    g.visited.add(grd.get_loc())

    while grd.ongrid:
        grd.step(g)
    
    rc_visited = {(r,c) for (r,c,d) in g.visited}
    #g.prn()
    print(f"visited: {len(rc_visited)}")

    return rc_visited

rcvs = p1()


def check_is_loop(g :Grid,grd: Guard):

    while grd.ongrid and not grd.inloop:
        grd.step(g)

    return grd.inloop


#lines = parse_input("day06ex.txt")
lines = parse_input("day06in.txt")
ref_grid = Grid(lines)
g = Grid(lines)
ref_grd = find_guard(g)
ref_guard = find_guard(g)
rcs = [(r,c) for r,c in rcvs if ref_grid.G[r][c] != "#"]

def p2():

    def test_rc(rc):
        r,c = rc
        # reset grid
        g.visited.clear()

        # reset guard
        grd = Guard(ref_grd.r, ref_grd.c, Dir.N)

        g.visited.add(grd.get_loc())
        g.add_box((r,c))

        #grd = find_guard(g)
        is_loop = check_is_loop(g, grd)
        g.rm_box((r,c))

        return is_loop

    nloopers = 0

    t_0 = time.time()


    for rc in rcs:
        is_loop = test_rc(rc)
        if is_loop:
            r,c = rc
            nloopers += 1
            #print(f"looper: ({r:3d},{c:3d}), n: {nloopers}")

    t_1 = time.time()
    dt = t_1 - t_0
    print(f"dt = {dt} secs")
    print(f"found: {nloopers}")
p2()

    
    