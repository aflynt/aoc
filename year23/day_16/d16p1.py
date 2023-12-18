from enum import Enum


class Dir(Enum):
    #     r, c
    N = (-1, 0)
    S = ( 1, 0)
    E = ( 0, 1)
    W = ( 0,-1)

def get_lines(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip("\n") for line in lines]

    return lines

def get_grid(lines):
    G = [[c for c in row] for row in lines]

    return G


def print_grid(G):
    R = len(G)
    C = len(G[0])
    for r in range(R):
        ROW_CHARS = [G[r][c] for c in range(C)]
        ROW_STR = "".join(ROW_CHARS)
        print(ROW_STR)

class Beam:
    def __init__(self, r, c, dir, G):
        self.r = r
        self.c = c
        self.dir = dir
        self.G = G
        self.R = len(G)
        self.C = len(G[0])
    def __str__(self) -> str:
        return f"{self.r}_{self.c}_{self.dir.name}"
    def __repr__(self) -> str:
        return self.__str__()
    def get_pos(self):
        return (self.r, self.c)
    def mv(self):
        mv_dir = self.dir.value
        direction = self.dir
        nr = self.r + mv_dir[0]
        nc = self.c + mv_dir[1]
        G = self.G
        if nr < 0 or nr >= self.R:
            return None
        if nc < 0 or nc >= self.C:
            return None
        next_char = self.G[nr][nc]
        if next_char == ".":
            # continue
            return [Beam(nr,nc, self.dir, G)]
        elif next_char == "/":
            if   self.dir == Dir.E: return [Beam(nr,nc, Dir.N, G)]
            elif self.dir == Dir.W: return [Beam(nr,nc, Dir.S, G)]
            elif self.dir == Dir.N: return [Beam(nr,nc, Dir.E, G)]
            else                  : return [Beam(nr,nc, Dir.W, G)]
        elif next_char == '\\':
            if   self.dir == Dir.E: return [Beam(nr,nc, Dir.S, G)]
            elif self.dir == Dir.W: return [Beam(nr,nc, Dir.N, G)]
            elif self.dir == Dir.N: return [Beam(nr,nc, Dir.W, G)]
            else                  : return [Beam(nr,nc, Dir.E, G)]
        elif next_char == '-':
            if   self.dir == Dir.E: return [Beam(nr,nc, Dir.E, G)]
            elif self.dir == Dir.W: return [Beam(nr,nc, Dir.W, G)]
            elif self.dir == Dir.N: return [Beam(nr,nc, Dir.W, G), Beam(nr,nc, Dir.E, G)]
            else                  : return [Beam(nr,nc, Dir.W, G), Beam(nr,nc, Dir.E, G)]
        elif next_char == '|':
            if   self.dir == Dir.E: return [Beam(nr,nc, Dir.N, G), Beam(nr,nc, Dir.S, G)]
            elif self.dir == Dir.W: return [Beam(nr,nc, Dir.N, G), Beam(nr,nc, Dir.S, G)]
            elif self.dir == Dir.N: return [Beam(nr,nc, Dir.N, G)]
            else                  : return [Beam(nr,nc, Dir.S, G)]


def find_energized(G, bmax=100):

    visited = set()
    bs = [Beam(0,-1, Dir.E, G)]
    n_bs = 1
    #while n_bs < bmax:
    for i in range(bmax):
        #if i % 10000 == 0:
        print(f"{i:4d}: {n_bs} {len(visited)}")
        new_bs = []


        # move beams
        for b in bs:
            moved_beams = b.mv()
            #print(f"{b} -> {moved_beams}")
            if moved_beams:
                new_bs += moved_beams

        # update beam list
        bs = new_bs
        n_bs = len(bs)

        # record current positions
        positions = [b.get_pos() for b in bs]
        positions = set(positions)
        visited |= positions

    return len(visited)


fname = ["ex.txt", "in.txt"][1]
lines = get_lines(fname)

G = get_grid(lines)

#eprint_grid(G)

print(find_energized(G, 1000))
#print(find_energized(G, 1e3))
#print(find_energized(G, 1e4))
#print(find_energized(G, 1e5))