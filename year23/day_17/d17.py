from lib import *
from queue import PriorityQueue

#fname = "ex.txt"
#fname = "ex2.txt"
fname = "in.txt"
G = get_grid(fname)
R = len(G)
C = len(G[0])

# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n
def A_Star(start: Node, goal: Node, dmin=4, dmax=10):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or pqueue
    openSet = PriorityQueue()

    # empty map of cameFrom[n] -> node before n
    cameFrom = {}

    # For node n, gScore[n] is cost of cheapest path from start to n currently known.
    gScore = init_gscore( R, C, dmax)
    gScore[start] = 0

    # For node n, fScore[n]: gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore = init_fscore( R, C, dmax)
    fScore[start] = h(start, goal)
    openSet.put((fScore[start], start))

    while not openSet.empty():

        _, cn = openSet.get() # get current node

        if (cn.r,cn.c) == (goal.r, goal.c):
            if dmin <= cn.mvs <= dmax:
                return reconstruct_path(cameFrom, cn)

        #nbrs = get_node_nbrs(G, cn)
        nbrs = get_node_nbrs_min_max(G, cn, dmin, dmax)

        for nbr in nbrs:
            # d(cn,nbr) = weight of edge from current to neighbor
            # tentative gScore is distance from start to nbr thru current node
            tentative_gScore = gScore[cn] + d(nbr, G)

            if tentative_gScore < gScore[nbr]:
                # this path to nbr is better than any previous one. Record it!
                cameFrom[nbr] = cn
                gScore[nbr] = tentative_gScore
                fScore[nbr] = tentative_gScore + h(nbr, goal)
                f = fScore[nbr]
                openSet.put((f,nbr))
                
        
def get_path_cost(nodes: list[Node], sn: Node):
    # sn = start node
    ans = 0
    for node in nodes:
        val = 0
        if node != sn:
            val = d(node, G)
        
        ans += val
    return ans

def print_nodes(nodes: list[Node]):
    for node in reversed(nodes):
        print(f"{node}")


################################################

#         r, c, mvs, dir 
#node = ( 0, 0,   0, Dir.E)
# IDK WHICH Starting dir is better
sn_e = Node(   0,   0, 0, Dir.E )
sn_s = Node(   0,   0, 0, Dir.S )
gn   = Node( R-1, C-1, 0, Dir.N ) # goal node r,c valid

print(f"Part 1")
nodes_e = A_Star(sn_e, gn, -1, 3)
nodes_s = A_Star(sn_s, gn, -1, 3)

ans_e = get_path_cost(nodes_e, sn_e)
ans_s = get_path_cost(nodes_s, sn_s)
print(f"starting E: {ans_e}, starting S: {ans_s}")

print(f"Part 2")
nodes_e = A_Star(sn_e, gn)
nodes_s = A_Star(sn_s, gn)

ans_e = get_path_cost(nodes_e, sn_e)
ans_s = get_path_cost(nodes_s, sn_s)
print(f"starting E: {ans_e}, starting S: {ans_s}")

#print_nodes(nodes)