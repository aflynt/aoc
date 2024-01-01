import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from collections import defaultdict


class Grid:
    def __init__(self, G, undirected = False) -> None:
        self.G = G
        self.R = len(G)
        self.C = len(G[0])
        self.sc = [ci for ci,c in enumerate(G[0]) if c == "."][0]
        self.ec = [ci for ci,c in enumerate(G[self.R-1]) if c == "."][0]
        self.undirected = undirected
        self.nodes = self.get_nodes()
        self.edges = self.get_edges()

    def get_nbrs(self,r,c):
        nbrs = ["#" for i in range(4)]
        deltas = [(-1,0), (1,0), (0,1), (0,-1)]
        for i,d in enumerate(deltas):
            dr,dc = d
            if 0 <= r+dr<self.R and 0<= c+dc<self.C:
                # ok to access this neighbor
                nbrs[i] = self.G[r+dr][c+dc]
        return nbrs

    def get_nbrs_indices(self,r,c):
        nbrs = []
        deltas = [(-1,0), (1,0), (0,1), (0,-1)]
        for dr,dc in deltas:
            if 0 <= r+dr<self.R and 0<= c+dc<self.C:
                # ok to access this neighbor
                nbrs.append((r+dr,c+dc))
        return nbrs


    def print(self) -> None:
        ilist = [ str(i%10) for i in range(self.C)]
        colstr = "".join(ilist)
        print("  |"+colstr)

        for r,line in enumerate(self.G):
            lstr = "".join(line)
            print(f"{r:2d}|{lstr}")

    def get_nodes(self)->list[tuple[int,int]]:
        nodes = []
        for r in range(1,self.R):
            for c in range(1,self.C):
                ival = self.G[r][c]
                nbrs = self.get_nbrs(r,c)
                nslopes = 0
                for n in nbrs:
                    if n == "v" or n == ">":
                        nslopes += 1
                if nslopes >= 3:
                    nodes.append((r,c))
        nodes.insert(0, (0,self.sc))
        nodes.append((self.R-1,self.ec))
        return nodes.copy()

    def get_edges(self):
        undirected = self.undirected
        Es = defaultdict(list)
        vs = self.get_nodes()

        for vi in vs:
            ri,ci = vi
            nbr_cs = self.get_nbrs(ri,ci)
            nbr_ee = nbr_cs[2]
            nbr_ss = nbr_cs[1]
            
            if nbr_ee == ">":
                cnt,rj,cj = self.dfs((ri,ci+1),1, {(ri,ci)})
                Es[(ri,ci)].append(((rj,cj), -cnt))
                if undirected:
                    Es[(rj,cj)].append(((ri,ci), -cnt))
            if nbr_ss == "v" or nbr_ss == ".":
                cnt,rj,cj = self.dfs((ri+1,ci),1, {(ri,ci)})
                Es[(ri,ci)].append(((rj,cj), -cnt))
                if undirected:
                    Es[(rj,cj)].append(((ri,ci), -cnt))

        return Es

    
    def dfs(self, v, start_cnt=0, start_seen=set()):
        S = [v]
        SEEN = set()
        start_seen = set(start_seen)
        SEEN |= start_seen
        count = start_cnt
        r,c = v
        while len(S) > 0:
            v = S.pop()
            r,c = v
            if v not in SEEN:
                SEEN |= {v} # label v as discovered
                count += 1
                ival = self.G[r][c]
                if ival == ">" and count > 2:
                    return count,r,c+1
                elif ival == "v" and count > 2:
                    return count,r+1,c
                elif ival == "." and r == self.R-1:
                    return count-1, r,c
                else:
                    nbr_idxs = self.get_nbrs_indices(r,c)
                    for nbr_idx in nbr_idxs:
                        r,c = nbr_idx
                        nval = self.G[r][c]
                        if nval != "#":
                            S.append(nbr_idx)
                # for all edges from v to w in G.adjacentEdges(v) do
                #   S.push(w)
        return count,r,c
        

def run_dfs(g: Grid):

    E = g.get_edges()
    start = (0,g.sc)

    ans = 0
    SEEN = [[False for _ in range(g.C)] for _ in range(g.R)]
    def dfs(v,d):
        nonlocal ans
        r,c = v
        if SEEN[r][c]:
            return
        SEEN[r][c] = True
        if r == g.R-1:
            ans = max(ans, d)
        for (y,yd) in E[v]:
            dfs(y,d-yd)
        SEEN[r][c] = False
    dfs(start,0)
    return ans

def get_input(fname: str, undirected=False) -> Grid:
    lines = open(fname, "r").read().strip("\n").split("\n")
    G = [[c for c in line] for line in lines]
    g = Grid(G,undirected)
    return g


def write_tha_graph(g:Grid):

    vs = g.get_nodes()
    es = g.get_edges()
    ebunch = []
    for k,w in es.items():
        rf,cf,rt,ct = k
        ebunch.append(((rf,cf), (rt,ct), {"weight": w}))


    G = nx.DiGraph()
    G.add_nodes_from(vs)
    G.add_edges_from(ebunch)

    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw(G, pos=pos)
    write_dot(G, 'file.dot')
