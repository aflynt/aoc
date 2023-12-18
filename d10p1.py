
def get_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    
    lines = [line.strip('\n') for line in lines]

    G = []

    for line in lines:
        chars = [ char for char in line]
        G.append(chars)

    return G

class Tile:
    def __init__(self, G, r, c):
        self.G = G
        self.r = r
        self.c = c
        self.ty = G[r][c]
        char = self.ty
        if   char == "|": nsew = (1,1,0,0)
        elif char == "-": nsew = (0,0,1,1)
        elif char == "L": nsew = (1,0,1,0)
        elif char == "J": nsew = (1,0,0,1)
        elif char == "7": nsew = (0,1,0,1)
        elif char == "F": nsew = (0,1,1,0)
        elif char == ".": nsew = (0,0,0,0)
        else: nsew = (1,1,1,1) # S
        self.nsew = nsew
        #n = self.nsew[0]
        #s = self.nsew[1]
        #e = self.nsew[2]
        #w = self.nsew[3]
    def __str__(self):
        ty = self.ty
        r = self.r
        c = self.c
        return f"{r:03d}_{c:03d}_{ty}"
    def __repr__(self):
        return f"Tile(G, {self.r},{self.c})"
    def get_rc(self):
        return (self.r,self.c)
    def connects_to_n(self):
        return self.nsew[0] == 1
    def connects_to_s(self):
        return self.nsew[1] == 1
    def connects_to_e(self):
        return self.nsew[2] == 1
    def connects_to_w(self):
        return self.nsew[3] == 1


def find_s(G):
    for i,row in enumerate(G):
        for j,char in enumerate(row):
            if char == 'S':
                return (i,j)

def get_valid_neighbors(si,sj):
    tn = Tile(G, si-1,sj)
    ts = Tile(G, si+1,sj)
    te = Tile(G, si  ,sj+1)
    tw = Tile(G, si  ,sj-1)
    nbrs = {'N': tn, 'S': ts, 'E': te, 'W': tw}
    ti = Tile(G, si, sj)
    
    valid_nbrs = []
    for k,v in nbrs.items():
        if k == 'N': isvalid = v.connects_to_s() and ti.connects_to_n()
        if k == 'S': isvalid = v.connects_to_n() and ti.connects_to_s()
        if k == 'E': isvalid = v.connects_to_w() and ti.connects_to_e()
        if k == 'W': isvalid = v.connects_to_e() and ti.connects_to_w()
        if isvalid:
            valid_nbrs.append(v)
    return valid_nbrs

def get_next_tile(nt, lt):
    vns = get_valid_neighbors(nt.r,nt.c)
    vn0 = vns[0]
    vn1 = vns[1]
    ltrc = lt.get_rc()
    vn0_rc = vn0.get_rc()
    vn0_last = vn0_rc == ltrc
    lt = nt
    nt = vn0 if not vn0_last else vn1
    return nt, lt

#fname = 'ex_10.txt'
fname = 'in_10.txt'

G  = get_input(fname)

(si,sj) = find_s(G)
start_tile = Tile(G, si, sj)

vns = get_valid_neighbors(si,sj)

steps = 1

lt0 = start_tile # last tile
lt1 = start_tile # last tile
nt0 = vns[0] # next tile
nt1 = vns[1] # next tile

same_same = nt0.get_rc() == nt1.get_rc()

while not same_same:
    nt0, lt0 = get_next_tile(nt0,lt0)
    nt1, lt1 = get_next_tile(nt1,lt1)
    steps += 1
    print(f"from {lt0} -> {nt0}, {lt1} -> {nt1}, steps: {steps}")
    same_same = nt0.get_rc() == nt1.get_rc()

