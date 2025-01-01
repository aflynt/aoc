from enum import Enum
from time import sleep

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
        self.lrings = set()
        self.rrings = set()
        self.xpos = (0,0)
        self.find_xpos()
        self.clear_rings()
        self.clear_xpos()
    def at(self,r,c):
        v = self.G[r][c]
        if (r,c) in self.rings:
            v = "O"
        elif (r,c) in self.rrings:
            v = "]"
        elif (r,c) in self.lrings:
            v = "["
        elif (r,c) == self.xpos:
            v = "@"
        return v
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
                elif v == "[":
                    self.lrings.add((r,c))
                elif v == "]":
                    self.rrings.add((r,c))
    def clear_rings(self):
        for ring in self.rrings:
            r,c = ring
            self.G[r][c] = "."
        for ring in self.lrings:
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
                elif (r,c) in self.rrings:
                    v = "]"
                elif (r,c) in self.lrings:
                    v = "["
                elif (r,c) == self.xpos:
                    v = "@"
                #print(v,end=" ")
                print(v,end="")
            print()

    def shift_rings(self, dr,dc, mvs):
        # get LR target mv lrings, rrings
        slrings = mvs&self.lrings
        srrings = mvs&self.rrings

        # remove shifted rings
        self.lrings -= slrings
        self.rrings -= srrings

        # shift rings
        slrings = [(r+dr,c+dc) for r,c in slrings]
        srrings = [(r+dr,c+dc) for r,c in srrings]

        # add rings back
        self.lrings |= set(slrings)
        self.rrings |= set(srrings)

        # move xpos
        xr,xc = self.xpos
        self.xpos = (xr+dr, xc+dc)

    def can_mv(self, src, dest):
        er = dest[0]
        ec = dest[1]
        sr = src[0]
        sc = src[1]
        dr = er - sr
        dc = ec - sc
        #dir = "E"
        #if   dr < 0: dir = "N"
        #elif dr > 0: dir = "S"
        #elif dc < 0: dir = "W"
        destval = self.at(er,ec)

        dest_empty = dest not in self.lrings \
                 and dest not in self.rrings \
                 and dest not in self.boxes

        if dest_empty:
            return True
        elif dest in self.boxes:
            return False
        elif destval == "[" and dc == 0: # N/S
            # need to move both sides of ring
            can_mv_L = self.can_mv((er,ec  ), (er+dr, ec  ))
            can_mv_R = self.can_mv((er,ec+1), (er+dr, ec+1))
            return can_mv_L and can_mv_R
        elif destval == "]" and dc == 0: # N/S
            can_mv_L = self.can_mv((er,ec  ), (er+dr, ec  ))
            can_mv_R = self.can_mv((er,ec-1), (er+dr, ec-1))
            return can_mv_L and can_mv_R
        elif destval == "[" or destval == "]":
            can_mv_LR = self.can_mv((sr,ec+dc),(sr,ec+2*dc))
            return can_mv_LR
        else:
            assert False, "bad case of destval..."

    def collect_moves(self, src, dest, mvs=set()):
        er = dest[0]
        ec = dest[1]
        sr = src[0]
        sc = src[1]
        dr = er - sr
        dc = ec - sc
        destval = self.at(er,ec)
        mvs.add((sr,sc))

        dest_empty = dest not in self.lrings \
                 and dest not in self.rrings \
                 and dest not in self.boxes

        if dest_empty:
            mvs.add((sr,sc))
            return mvs
        elif destval == "[" and dc == 0: # N/S
            # need to move both sides of ring
            mvs.add((er,ec))
            mvs.add((er,ec+1))
            mvs_L = self.collect_moves((er,ec  ), (er+dr, ec  ), mvs)
            mvs_R = self.collect_moves((er,ec+1), (er+dr, ec+1), mvs)
            mvs |= mvs_L | mvs_R
            return mvs
        elif destval == "]" and dc == 0: # N/S
            mvs.add((er,ec))
            mvs.add((er,ec-1))
            mvs_L = self.collect_moves((er,ec  ), (er+dr, ec  ), mvs)
            mvs_R = self.collect_moves((er,ec-1), (er+dr, ec-1), mvs)
            mvs |= mvs_L | mvs_R
            return mvs
        elif destval == "[" or destval == "]":
            # se
            # @[].
            mvs.add((sr,sc))
            mvs.add((sr,ec))
            mvs.add((sr,ec+dc))
            mvs_LR = self.collect_moves((sr,ec+dc),(sr,ec+2*dc), mvs)
            mvs |= mvs_LR
            return mvs
        else:
            assert False, "bad case of destval..."


    def mv_n(self):
        xr,xc = self.xpos

        can_mv = self.can_mv((xr,xc), (xr-1,xc))
        if can_mv:
            mvs = set()
            mvs = self.collect_moves((xr,xc), (xr-1,xc), mvs)
            #print(f"CAN MV? {can_mv}, mvs = {mvs}")
            self.shift_rings(-1, 0, mvs)

    def mv_s(self):
        xr,xc = self.xpos
        can_mv = self.can_mv((xr,xc), (xr+1,xc))
        if can_mv:
            mvs = set()
            mvs = self.collect_moves((xr,xc), (xr+1,xc), mvs)
            #print(f"CAN MV? {can_mv}, mvs = {mvs}")
            self.shift_rings(1,0, mvs)

    def mv_e(self):
        xr,xc = self.xpos
        can_mv = self.can_mv((xr,xc),(xr,xc+1))
        if can_mv:
            mvs = set()
            mvs = self.collect_moves((xr,xc), (xr,xc+1), mvs)
            #print(f"CAN MV? {can_mv}, mvs = {mvs}")
            self.shift_rings(0,1,mvs)

    def mv_w(self):
        xr,xc = self.xpos
        can_mv = self.can_mv((xr,xc),(xr,xc-1))
        if can_mv:
            mvs = set()
            mvs = self.collect_moves((xr,xc), (xr,xc-1), mvs)
            #print(f"CAN MV? {can_mv}, mvs = {mvs}")
            self.shift_rings(0,-1, mvs)


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
                elif rc in self.rrings:
                    v = "]"
                elif rc in self.lrings:
                    v = "["
                elif rc == self.xpos:
                    v = "@"
                else:
                    v = self.G[r][c]
                #rstr += f"{v} "
                rstr += f"{v}"
            rstr += "\n"
        return rstr



def read_file(fname, is_p2=False):

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
            if is_p2:
                wide_chars = []
                for c in chars:
                    if c == "#":
                        wide_chars.append("#")
                        wide_chars.append("#")
                    elif c == "O":
                        wide_chars.append("[")
                        wide_chars.append("]")
                    elif c == ".":
                        wide_chars.append(".")
                        wide_chars.append(".")
                    elif c == "@":
                        wide_chars.append("@")
                        wide_chars.append(".")
                    else:
                        assert False, "bad char type read"
                chars = wide_chars
            G.append(chars)
        else:
            for c in line:
                ins.append(c)

    g = Grid(G)
    ins = Instructions(ins)

    return g,ins

def p1():
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

#--------------------------------
fname = "ex15s.txt"
fname = "ex15l.txt"
fname = "in15.txt"

g,ins = read_file(fname, True)

print(g)

i = ins.pop()

while i:
    #print(f" i = {i}")
    #x = input()
    #sleep(1/5)
    g.move(i)
    #g.print()
    i = ins.pop()

g.print()

ans = 0
for ring in g.lrings:
    r,c = ring
    ans += 100*r + c


print(f"ans = {ans}")


"""
"""
