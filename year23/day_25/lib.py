import networkx as nx
import matplotlib.pyplot as plt
import pydot
from collections import defaultdict

def get_tightest_connected_vertex(G: nx.Graph, A:list[int]) -> int:
    V = set(G)
    V = { vi for vi in V if vi not in A}

    z = list(V)[0]
    maxwt = 0
    for y in V:
        wtsum = 0
        for Ai in A:
            w = 0
            try:
                w =  G[Ai][y]["weight"]
                wtsum += w
            except:
                wtsum += 0
        if wtsum > maxwt:
            z = y
            maxwt = wtsum
    return z

def min_cut_phase(G: nx.Graph,a:int, cops:list[int]):

    V = set(G)
    A = [a]
    while len(A) < len(V):
        z = get_tightest_connected_vertex(G,A)
        A.append(z)
    
    s = A[-2]
    t = A[-1]

    print(f"found s: {s}")
    print(f"found t: {t}")

    # store cut of phase
    cut_wt = 0
    for n in G[t]:
        cut_wt += G[t][n]['weight']
    cops.append((cut_wt, t))

    # shrink G by mergin the two vertices added last
    # find nodes adjacent to t

    nbrs_s = G[s]
    nbrs_t = G[t]

    nbrs_st = [n for n in nbrs_s if n in nbrs_t]
    nbrs_s = [n for n in nbrs_s if n != t and n not in nbrs_st]
    nbrs_t = [n for n in nbrs_t if n != s and n not in nbrs_st]

    new_node_name = f"{s},{t}"
    new_nbr_edges = []
    # link to s & t
    for n in nbrs_st:
        wt = G[t][n]['weight'] + G[s][n]['weight']
        new_nbr_edges.append((new_node_name, n, {'weight': wt}))
    # single link to s
    for n in nbrs_s:
        wt = G[s][n]['weight']
        new_nbr_edges.append((new_node_name, n, {'weight': wt}))
    # single link to t
    for n in nbrs_t:
        wt = G[t][n]['weight']
        new_nbr_edges.append((new_node_name, n, {'weight': wt}))

    G.remove_node(t)
    G.remove_node(s)
    G.add_node(new_node_name)
    G.add_edges_from(new_nbr_edges)

    return cops,G

def min_cut(G: nx.Graph, a: int):
    cop = []
    while len(set(G)) > 1:
        cop,G = min_cut_phase(G, a, cop)
        #print(f"cop = {cop}")
    return cop