from collections import deque

lines = open("ex18.txt", "r").read().split()
#lines = open("in18.txt", "r").read().split()
lines = [line.strip() for line
         in lines]
bs = []
for line in lines:
    a,b = line.split(",")
    bs.append((int(a),int(b)))

class Grid:
    def __init__(self, bs=[], R=7, C=7, nfall=12):
        self.R = R
        self.C = C
        self.bs = bs
        self.G = []
        self.nfall = nfall
        for r in range(self.R):
            cs = ["." for _ in range(self.C)]
            self.G.append(cs)
        for n in range(self.nfall):
            if n < len(self.bs):
                bn = self.bs[n]
                c,r = bn
                self.G[r][c] = "#"

    def prn(self):
        cnums = [str(i%10) for i in range(self.C)]
        cstr = "".join(cnums)
        line_str = "_"*self.C
        #print(f"  0123456")
        print(f"   {cstr}")
        print(f"   {line_str}")
        for r in range(self.R):
            line_str = "".join(self.G[r])
            print(f"{r:2d}|{line_str}")

    def write_path(self, path):
        for prc in path:
            r,c = prc
            self.G[r][c] = "O"

    def bfs(self):
        node = (0,0)
        target = (self.R-1, self.C-1)

        visited = {}  # dict to store where the visit came from
        q = deque()    # Use a deque to not lose efficiency with pop(0)

        visited[node] = None
        q.append(node)

        while q:
            m = q.popleft()
            (r,c) = m
            if m == target:  # Bingo!
                # Extract path from visited information
                path = []
                while m:
                    path.append(m)
                    m = visited[m]  # Walk back
                
                self.write_path(path)
                return path[::-1]  # Reverse it
            #        up     right   down   left
            drcs = [(-1,0), (0,1), (1,0), (0,-1)]
            nbrs = []
            for (dr,dc) in drcs:
                rr,cc = r+dr,c+dc
                if 0 <= rr < self.R and 0 <= cc < self.C:
                    if self.G[rr][cc] != "#":
                        nbrs.append((rr,cc))
            for nbr in nbrs:
                if nbr not in visited:
                    visited[nbr] = m  # Remember where we came from
                    q.append(nbr)


g = Grid(bs)
#g = Grid(bs, 71, 71, 1024)
path = g.bfs()
nsteps = len(path) - 1
print(f"steps: {nsteps}")
g.prn()
