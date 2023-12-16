
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
    def __lt__(self, other):
        return self.get_rc() < other.get_rc()
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

def get_path_tiles(start_tile, vns):

    lt0 = start_tile # last tile
    lt1 = start_tile # last tile
    nt0 = vns[0] # next tile
    nt1 = vns[1] # next tile
    path_tiles = set([start_tile.get_rc(), nt0.get_rc(), nt1.get_rc()])
    
    same_same = nt0.get_rc() == nt1.get_rc()
    
    while not same_same:
        nt0, lt0 = get_next_tile(nt0,lt0)
        nt1, lt1 = get_next_tile(nt1,lt1)
        same_same = nt0.get_rc() == nt1.get_rc()
        path_tiles.add(nt0.get_rc())
        path_tiles.add(nt1.get_rc())
    
    path_tiles = list(path_tiles)
    path_tiles = sorted(path_tiles)

    return path_tiles

def get_count(r,c,tiles):
    l = ""
    cnt = 0
    if len(tiles) > 0:
        print(f"checking rc = {r:2d},{c:2d}, Tiles = {tiles},  cntbars: {cnt_bars} ")
        for t in tiles:
            if l == "" and t == "|":
                    cnt += 1
            elif l == "" and t in ["F","7", "L", "J"]:
                    cnt += 1
            elif l in ["F","7", "L", "J"] and t == "|": # l = F7LJ
                    cnt += 2
            elif l in ["F","7", "L", "J"] and t in ["F","7", "L", "J"]: # l = F7LJ
                    cnt += 0

            print(f"t: {t}, state: {cnt}")

    return cnt

def get_tiles_inside(G, path_tiles):
    tiles_in = set()
    
    # iterate over every point
    for r,row in enumerate(G):
        for c, char in enumerate(row):
            if (r,c) in path_tiles:
                continue
    
            # mk list of Tiles between r,c and (r,0)
            tiles = [Tile(G,r,ci) for ci in range(c+1)]
    
            # count bar tiles in path_tiles
            #tiles = [t for t in tiles if t.get_rc() in path_tiles and t.ty == "|"]
            tiles = [t.ty for t in tiles if t.get_rc() in path_tiles]
            tiles = "".join(tiles)
            tiles = tiles.replace("-","")
            tiles = tiles.replace("S7","||") # hack
            cnt = get_count(r,c,tiles[::-1])
            #tiles = tiles.replace("FJ","||")
            #tiles = tiles.replace("LJ","||")
            #tiles = tiles.replace("F7","||")
            #tiles = tiles.replace("L7","||")
            bars = [c for c in tiles if c == "|"]
            cnt_bars = len(bars)
            ntiles = len(tiles)
            iseven = ntiles % 2 == 0
            #if not iseven and not isvert_even:
            if not iseven:
                tiles_in.add((r,c))

#fname = 'ex_10a.txt'
fname = 'ex_10a.txt'
#fname = 'ex_10b.txt'
#fname = 'in_10.txt'

G  = get_input(fname)

(si,sj) = find_s(G)
start_tile = Tile(G, si, sj)
print(f"found start tile: {start_tile}")

vns = get_valid_neighbors(si,sj)

print(f"valid neighbors: {vns}")
cn = start_tile.connects_to_n()
cs = start_tile.connects_to_s()
ce = start_tile.connects_to_e()
cw = start_tile.connects_to_w()

print(f"cn = {cn}")
print(f"cs = {cs}")
print(f"ce = {ce}")
print(f"cw = {cw}")

#path_tiles = get_path_tiles(start_tile, vns)
#for pt in path_tiles:
#    print(pt)


#for ti in tiles_in:
#    print(ti)
#
## 5 for example
#print(len(tiles_in))