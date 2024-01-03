from lib import *

#fname = "ex.txt"
fname = "in.txt"
lines = open(fname, "r").read().strip("\n").split("\n")

connections = defaultdict(list)
for line in lines:
    name,cons = line.split(": ")
    cons = cons.split(" ")
    connections[name] += cons

G = nx.Graph()

for n in connections.keys():
    G.add_node(n)

for k,v in connections.items():
    for nbr in v:
        G.add_edge(k,nbr, weight=1)
        G.add_edge(nbr,k, weight=1)



NR = 727
nnodes = G.number_of_nodes()
NL = nnodes - NR

ans = NR * NL
print(f"N_NODES = {nnodes}")
print(f"NR  = {NR}")
print(f"NL  = {NL}")
print(f"ans = {ans}")


#start_node = list(connections.keys())[0]
#print(f"starting_with : {start_node}")

#cop = min_cut(G, start_node)
#cop = sorted(cop)[0:3]
#print(f"mincut: {cop}")