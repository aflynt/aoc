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

for n in G:
    nbr = G[n]
    print(f"{n} -> {nbr}")

#V = [1,2,3,4,5,6,7,8,]
#G.add_nodes_from(V)

#ws = [
#    (1,2, {'weight':2}),
#    (1,5, {'weight':3}),
#    (2,3, {'weight':3}),
#    (2,5, {'weight':2}),
#    (2,6, {'weight':2}),
#    (3,4, {'weight':4}),
#    (3,7, {'weight':2}),
#    (4,7, {'weight':2}),
#    (4,8, {'weight':2}),
#    (5,6, {'weight':3}),
#    (6,7, {'weight':1}),
#    (7,8, {'weight':3}),
#]
#G.add_edges_from(ws)

#ax = plt.figure()
#ax = plt.subplot(111)
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()


start_node = list(connections.keys())[0]
print(f"starting_with : {start_node}")

cop = min_cut(G, start_node)

cop = sorted(cop)[0:3]

print(f"mincut: {cop}")