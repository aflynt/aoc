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

def get_rc_tiles(r, c, R, C):

    tr = (r - (r % R )) // R
    tc = (c - (c % C )) // C
    return (tr, tc)

def get_start(G: Grid):
    for i in range(G.R):
        for j in range(G.C):
            if G.at(i,j) == "S":
                return (i,j)
    return (-1,-1)