from lib import *
from queue import PriorityQueue

#fname = "ex.txt"
fname = "in.txt"
G = get_grid(fname)
R = len(G)
C = len(G[0])
#gr = R-1 # goal row
#gc = C-1 # goal col

# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n
def A_Star(start: Node, goal: Node):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or pqueue
    openSet = []
    #openSet = PriorityQueue()
    #openSet.put((0,start)) # TODO: do i chg to (fscore, node)? how does it get sorted?

    # empty map of cameFrom[n] -> node before n
    cameFrom = {}

    # For node n, gScore[n] is cost of cheapest path from start to n currently known.
    gScore = init_gscore( R, C)
    gScore[start] = 0

    # For node n, fScore[n]: gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore = init_fscore( R, C)
    fScore[start] = h(start, goal)
    #openSet.put((fScore[start], start))
    openSet.append((fScore[start], start))

    i = 0

    #while not openSet.empty():
    while len(openSet) > 0:
        i += 1
        print(i)
        if i > 12000:
            break

        #_, cn = openSet.get() # get current node
        openSet = sorted(openSet, reverse=True)
        _, cn = openSet.pop() # get current node

        if (cn.r,cn.c) == (goal.r, goal.c):
            return reconstruct_path(cameFrom, cn)

        nbrs = get_node_nbrs(G, cn)

        for nbr in nbrs:
            #key_nbr = (nbr.r, nbr.c, nbr.mvs, nbr.dir)
            # d(cn,nbr) = weight of edge from current to neighbor
            # tentative gScore is distance from start to nbr thru current node
            tentative_gScore = gScore[cn] + d(nbr, G)

            if tentative_gScore < gScore[nbr]:
                # this path to nbr is better than any previous one. Record it!
                cameFrom[nbr] = cn
                gScore[nbr] = tentative_gScore
                fScore[nbr] = tentative_gScore + h(nbr, goal)
                f = fScore[nbr]
                if (f,nbr) not in openSet:
                    #openSet.put((f,nbr))
                    openSet.append((f,nbr))
                
        


        


################################################

#      f, r, c, mvs, dir 
#epos = (0, 0, 0, 0, Dir.E)
sn = Node(0,0,0,Dir.E)
gn = Node(R-1,C-1,0,Dir.N)
nodes = A_Star(sn, gn)

ans = 0
for node in nodes:
    val = 0
    if node != sn:
        val = d(node, G)
    
    ans += val
    print(f"val: {val:3d} sum: {ans:3d} node: {node}")

#
##ans = 0
#val = G[0][0]
#r = 0
#c = 0

#while True:
#    print(f"now at: ({r},{c}) val: {val}, ans: {ans}")
#    nbrs = get_nbrs(G, pos)
#    for i,nbr in enumerate(nbrs):
#        print(f"{i:2d} {nbr}")
#    pic = input("pick nbr #: ")
#    pic = int(pic)
#    pos = nbrs[pic]
#    print(f" -> new_pos = {pos}")
#    r = pos[1]
#    c = pos[2]
#    val = G[r][c]
#    ans += val


