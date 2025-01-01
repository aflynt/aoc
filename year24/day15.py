from enum import Enum

class Dir(Enum):
    def __init__(self) -> None:
        super().__init__()
        self.N = 0
        self.S = 1
        self.E = 2
        self.W = 3

class Instructions:
    def __init__(self, ins:list[str]) -> None:
        self.ins = ins
    def empty(self):
        return len(self.ins) == 0
    def peek(self):
        if not self.empty():
            return self.ins[0]
        return None
    def pop(self):
        if not self.empty():
            x = self.ins[0]
            self.ins = self.ins[1:]
            return x
        return None
    def push(self, x):
        self.ins.append(x)
    def __str__(self):
        i_str = "".join(self.ins)
        return i_str
    def __repr__(self) -> str:
        return f"I({self.ins})"

class Grid:
    def __init__(self,G) -> None:
        self.G = G
        self.R = len(G)
        self.C = len(G[0])
        self.boxes = set()
        self.rings = set()
        self.xpos = (0,0)
        self.find_xpos()
        self.clear_rings()
        self.clear_xpos()
    def at(self,r,c):
        return self.G[r][c]
    def find_xpos(self):
        for r in range(self.R):
            for c in range(self.C):
                v = self.at(r,c)
                if v == "@":
                    self.xpos = (r,c)
                elif v == "#":
                    self.boxes.add((r,c))
                elif v == "O":
                    self.rings.add((r,c))
    def clear_rings(self):
        for ring in self.rings:
            r,c = ring
            self.G[r][c] = "."
    def clear_xpos(self):
        r,c = self.xpos
        self.G[r][c] = "."
    def print(self):
        for r in range(self.R):
            for c in range(self.C):
                v = self.G[r][c]
                if (r,c) in self.rings:
                    v = "O"
                elif (r,c) == self.xpos:
                    v = "@"
                print(v,end=" ")
            print()
    def mv_n(self):
        xr,xc = self.xpos
        r0 = 0
        r1 = xr-1
        # find first rock == r0
        rbox = r1
        while rbox >= 0:
            if (rbox, xc) in self.boxes:
                break
            rbox -= 1
        r0 = rbox
        rs = range(r1,r0, -1)
        ci = xc
        e = -1
        for ri in rs:
            # find open slot
            is_box  = (ri,ci) in self.boxes
            is_ring = (ri,ci) in self.rings
            if not is_box and not is_ring:
                # appears to be open
                # move here
                e = ri
                break

        # can move
        if e > -1:
            # shift rings in the way
            #       e<-s
            # PRE   .OO@
            # POST  OO@
            # shifting north
            srs = set([(r,xc) for r in range(e,xr)])
            srings = srs&self.rings
            # isolated shifted rings
            self.rings -= srings
            # now shift up srings
            srings = [(r-1,c) for r,c in srings]
            # now add back to rings
            self.rings |= set(srings)
            # now move xpos
            self.xpos = (xr-1, xc)
    def mv_s(self):
        xr,xc = self.xpos
        r0 = xr+1   # first row is me + 1
        r1 = self.R # last row is bottom
        # find first rock between me and bottom
        rbox = r0
        while rbox < self.R:
            if (rbox, xc) in self.boxes:
                break
            rbox += 1
        r1 = rbox
        rs = range(r0,r1+1)
        ci = xc
        e = -1
        for ri in rs:
            # find open slot
            is_box  = (ri,ci) in self.boxes
            is_ring = (ri,ci) in self.rings
            if not is_box and not is_ring:
                # appears to be open
                # move here
                e = ri
                break

        # can move
        if e > -1:
            # shift rings in the way
            #       s_>e
            # PRE   @OO.
            # POST  .@OO
            # shifting north
            srs = set([(r,xc) for r in range(r0, e+1)])
            srings = srs&self.rings
            # isolated shifted rings
            self.rings -= srings
            # now shift up srings
            srings = [(r+1,c) for r,c in srings]
            # now add back to rings
            self.rings |= set(srings)
            # now move xpos
            self.xpos = (xr+1, xc)
    def mv_e(self):
        xr,xc = self.xpos
        c0 = xc+1    # c0 == start  search col
        c1 = self.C  # c1 == ending search col
        # find first rock between me and bottom
        cbox = c0
        while cbox < self.C:
            if (xr,cbox) in self.boxes:
                break
            cbox += 1
        c1 = cbox
        cs = range(c0,c1)
        ri = xr
        e = -1
        for ci in cs:
            # find open slot
            is_box  = (ri,ci) in self.boxes
            is_ring = (ri,ci) in self.rings
            if not is_box and not is_ring:
                # appears to be open
                # move here
                e = ci
                break

        # can move
        if e > -1:
            # shift rings in the way
            #       s_>e
            # PRE   @OO.
            # POST  .@OO
            # shifting north
            srs = set([(xr,c) for c in range(c0,e+1)])
            srings = srs&self.rings
            # isolated shifted rings
            self.rings -= srings
            # now shift up srings
            srings = [(r,c+1) for r,c in srings]
            # now add back to rings
            self.rings |= set(srings)
            # now move xpos
            self.xpos = (xr, xc+1)
    def mv_w(self):
        xr,xc = self.xpos
        c0 = 0
        c1 = xc-1
        # find first rock between me and edge
        cbox = c1
        while cbox >= 0:
            if (xr,cbox) in self.boxes:
                break
            cbox -= 1
        c0 = cbox
        cs = range(c1,c0, -1)
        ri = xr
        e = -1
        for ci in cs:
            # find open slot
            is_box  = (ri,ci) in self.boxes
            is_ring = (ri,ci) in self.rings
            if not is_box and not is_ring:
                # appears to be open
                # move here
                e = ci
                break

        # can move
        if e > -1:
            # shift rings in the way
            #       e<-s
            # PRE   .OO@
            # POST  OO@
            # shifting north
            srs = set([(xr,c) for c in range(e,xc)])
            srings = srs&self.rings
            # isolated shifted rings
            self.rings -= srings
            # now shift up srings
            srings = [(r,c-1) for r,c in srings]
            # now add back to rings
            self.rings |= set(srings)
            # now move xpos
            self.xpos = (xr, xc-1)


    def move(self, dir):
        match dir:
            case "^": self.mv_n()
            case "v": self.mv_s()
            case ">": self.mv_e()
            case "<": self.mv_w()

    def __str__(self) -> str:
        rstr = ""
        for r in range(self.R):
            for c in range(self.C):
                rc = (r,c)
                if rc in self.rings:
                    v = "O"
                elif rc == self.xpos:
                    v = "@"
                else:
                    v = self.G[r][c]
                rstr += f"{v} "
            rstr += "\n"
        return rstr



def read_file(fname):

    with open(fname, "r") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]

    G = []
    ins = []

    reading_grid = True
    for line in lines:
        if len(line) < 2:
            reading_grid = False
            continue
        if reading_grid:
            chars = [c for c in line]
            G.append(chars)
        else:
            for c in line:
                ins.append(c)

    g = Grid(G)
    ins = Instructions(ins)

    return g,ins



#--------------------------------
fname = "ex15l.txt"
fname = "ex15s.txt"
fname = "in15.txt"

g,ins = read_file(fname)

#print(g)

i = ins.pop()

while i:
    #print(f" i = {i}")
    #x = input()
    g.move(i)
    #g.print()
    i = ins.pop()

g.print()

ans = 0
for ring in g.rings:
    r,c = ring
    ans += 100*r + c


print(f"ans = {ans}")

