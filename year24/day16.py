
from collections import deque


class Grid:
    def __init__(self, G) -> None:
        self.G = G
        self.R = len(G)
        self.C = len(G[0])
        self.S = self.find_char("S")
        self.E = self.find_char("E")
        self.walls = set()
        self.find_walls()
    def at(self,r,c):
        v = self.G[r][c]
        return v
    def find_char(self, char):
        for r in range(self.R):
            for c in range(self.C):
                v = self.at(r,c)
                if v == char:
                    return (r,c)
        return (-1,-1)
    def find_walls(self):
        for r in range(self.R):
            for c in range(self.C):
                v = self.at(r,c)
                if v == "#":
                    self.walls.add((r,c))
    def print(self):
        for r in range(self.R):
            for c in range(self.C):
                v = self.G[r][c]
                print(v,end="")
            print()
    def __str__(self) -> str:
        rstr = ""
        for r in range(self.R):
            for c in range(self.C):
                v = self.at(r,c)
                rstr += f"{v}"
            rstr += "\n"
        return rstr
    def get_turn_price(self, facing, to_face):
        tpd = {
            # facing, to_face
            ("N","N"):  0*1000,
            ("N","S"):  2*1000,
            ("N","E"):  1*1000,
            ("N","W"):  1*1000,
            ("S","N"):  2*1000,
            ("S","S"):  0*1000,
            ("S","E"):  1*1000,
            ("S","W"):  1*1000,
            ("E","N"):  1*1000,
            ("E","S"):  1*1000,
            ("E","E"):  0*1000,
            ("E","W"):  2*1000,
            ("W","N"):  1*1000,
            ("W","S"):  1*1000,
            ("W","E"):  2*1000,
            ("W","W"):  0*1000,
        }
        f_to = (facing, to_face)
        match f_to:
            case ("N","N"): return 0*1000
            case ("N","S"): return 2*1000
            case ("N","E"): return 1*1000
            case ("N","W"): return 1*1000
            case ("S","N"): return 2*1000
            case ("S","S"): return 0*1000
            case ("S","E"): return 1*1000
            case ("S","W"): return 1*1000
            case ("E","N"): return 1*1000
            case ("E","S"): return 1*1000
            case ("E","E"): return 0*1000
            case ("E","W"): return 2*1000
            case ("W","N"): return 1*1000
            case ("W","S"): return 1*1000
            case ("W","E"): return 2*1000
            case ("W","W"): return 0*1000
            case _:
                assert False, "base facing, to_facing"

    def BFS(self):
        tpd = {
            # facing, to_face
            ("N","N"):  0*1000,
            ("N","S"):  2*1000,
            ("N","E"):  1*1000,
            ("N","W"):  1*1000,
            ("S","N"):  2*1000,
            ("S","S"):  0*1000,
            ("S","E"):  1*1000,
            ("S","W"):  1*1000,
            ("E","N"):  1*1000,
            ("E","S"):  1*1000,
            ("E","E"):  0*1000,
            ("E","W"):  2*1000,
            ("W","N"):  1*1000,
            ("W","S"):  1*1000,
            ("W","E"):  2*1000,
            ("W","W"):  0*1000,
        }
        tot_price = 10000000*self.R*self.C + 2
        #tot_price = 2e9
        visited = set()
        q = deque()
        dps = [
           ("E",   0),
           ("N",1000),
           ("S",1000),
           ("W",2000),
        ]
        for dp in dps:
            dir, price = dp
            q.append((self.S[0], self.S[1], dir, price))

        i = 1
        while q:
            rcdp = q.popleft()
            if rcdp not in visited:
                visited.add(rcdp)
                r,c,d,p = rcdp
                if i % 100000 == 0:
                    print(f"checking rcdp: {r:3d} {c:3d} {d} {p:10d}, lowP: {tot_price:,} lenQ: {len(q)}")
                if  p < tot_price and (r,c) == self.E:
                    # found a better path
                    tot_price = p
                else:
                    # keep searching
                    # add NSEW from here
                    can_go_N = self.G[r-1][c] != "#"
                    can_go_S = self.G[r+1][c] != "#"
                    can_go_E = self.G[r][c+1] != "#"
                    can_go_W = self.G[r][c-1] != "#"
                    #can_go_N = (r-1,c) not in self.walls
                    #can_go_S = (r+1,c) not in self.walls
                    #can_go_E = (r,c+1) not in self.walls
                    #can_go_W = (r,c-1) not in self.walls
                    if can_go_N:
                        #p_N = p + 1 + self.get_turn_price(d,"N")
                        p_N = p + 1 + tpd[(d,"N")]
                        new_rcdp = (r-1,c,'N',p_N)
                        if p_N < tot_price and new_rcdp not in visited:
                            q.append(new_rcdp)
                    if can_go_S:
                        #p_S = p + 1 + self.get_turn_price(d,"S")
                        p_S = p + 1 + tpd[(d,"S")]
                        new_rcdp = (r+1,c,'S',p_S)
                        if p_S < tot_price and new_rcdp not in visited:
                            q.append(new_rcdp)
                    if can_go_E:
                        #p_E = p + 1 + self.get_turn_price(d,"E")
                        p_E = p + 1 + tpd[(d,"E")]
                        new_rcdp = (r,c+1,'E',p_E)
                        if p_E < tot_price and new_rcdp not in visited:
                            q.append(new_rcdp)
                    if can_go_W:
                        #p_W = p + 1 + self.get_turn_price(d,"W")
                        p_W = p + 1 + tpd[(d,"W")]
                        new_rcdp = (r,c-1, 'W', p_W)
                        if p_W < tot_price and new_rcdp not in visited:
                            q.append(new_rcdp)
            i += 1

        return tot_price





def read_file(fname):

    with open(fname, "r") as f:
        lines = f.readlines()

    lines = [L.strip() for L in lines]

    G = []
    for line in lines:
        chars = [c for c in line]
        G.append(chars)

    g = Grid(G)

    return g


#--------------------------
fname = "ex16.txt"
fname = "ex162.txt"

g = read_file(fname)

g.print()

tp = g.BFS()
print(f"tot price = {tp}")


