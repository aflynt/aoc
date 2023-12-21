from queue import Queue

class Grid:
    def __init__(self, G):
        self.G = G
        self.R = len(G)
        self.C = len(G[0])
        self.rocks = set() 
        for i in range(self.R):
            for j in range(self.C):
                if self.G[i][j] == "#":
                    self.rocks.add((i,j))
    def at(self,i,j):
        return self.G[i][j]
    
    def print_grid(self):
        cchars = "".join([f"{c}" for c in range(self.C)])
        
        print(f"  |{cchars}")
        for i in range(self.R):
            print(f"{i:2d}|", end = "")
            for j in range(self.C):
                char = self.at(i,j)
                if char == ".":
                    char = "_"
                print(char, end="")
            print("|")
        print(f"  |{cchars}")
    def print_elf_grid(self, elf_locs):
        cchars = "".join([f"{c}" for c in range(self.C)])
        
        print(f"  |{cchars}")
        for i in range(self.R):
            print(f"{i:2d}|", end = "")
            for j in range(self.C):
                char = self.at(i,j)
                if (i,j) in elf_locs:
                    char = "O"
                print(char, end="")
            print("|")
        print(f"  |{cchars}")

        

class Elf:
    def __init__(self, pos):
        self.pos = pos
    def find_plots(self, G:Grid):
        plots = set()
        r,c = self.pos
        mvs = [(r+1,c), (r-1,c),(r,c+1),(r,c-1)]
        for rr,cc in mvs:
            if 0 <= rr < G.R and 0 <= cc < G.C and not (rr,cc) in G.rocks:
                plots.add((rr,cc))
        #print(f"plots: {plots}")
        return plots

def get_input(fname):
    lines = open(fname, "r").read().strip("\n")
    return lines.split("\n")

def get_grid(lines):
    
    G = []
    for i,row in enumerate(lines):
        rowvals = []
        for j,char in enumerate(row):
            rowvals.append(char)
        G.append(rowvals)
    return G

def get_start(G: Grid):
    for i in range(G.R):
        for j in range(G.C):
            if G.at(i,j) == "S":
                return (i,j)
    return (-1,-1)
        

################################################

fname = ["in.txt","ex.txt"][0]
lines = get_input(fname)
G = Grid(get_grid(lines))
plts_nxt = set([get_start(G)])


NMAX = 64
for i in range(NMAX):
    plts_now = plts_nxt
    plts_nxt = set()
    
    for plt in plts_now:
        plts_nxt |= Elf(plt).find_plots(G) # check its reachable plots

    print(f"step: {i+1:2d} n_plots: {len(plts_nxt)}")
    #G.print_elf_grid(elf_locs)
