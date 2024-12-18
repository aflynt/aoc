
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
