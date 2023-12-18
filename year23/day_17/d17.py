from lib import *
from queue import PriorityQueue

fname = "ex.txt"
G = get_grid(fname)
R = len(G)
C = len(G[0])
#gr = R-1 # goal row
#gc = C-1 # goal col

# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n
def A_Star(start, goal, h):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or pqueue
    openSet = PriorityQueue()
    openSet.put(start)

    # empty map of cameFrom[n] -> node before n
    cameFrom = {}

    # For node n, gScore[n] is cost of cheapest path from start to n currently known.
    #gScore = init_gscore(start, R, C)
    gScore = {} # defaults = infinity??
    gScore[start] = 0

    # For node n, fScore[n]: gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    #fScore = init_fscore(start, R, C)
    fScore = {} # defaults = infinity??
    fScore[start] = h(start, R, C)

    while not openSet.empty():
        cn = openSet.get() # get current node
        cr = cn[1]
        cc = cn[2]
        if (cr,cc) == (R-1, C-1):
            return reconstruct_path(cameFrom, cn)

        nbrs = get_nbrs(G, cn)
        


        


################################################

#      f, r, c, mvs, dir 
pos = (0, 0, 0, 0, Dir.E)

ans = 0
val = G[0][0]
r = 0
c = 0

while True:
    print(f"now at: ({r},{c}) val: {val}, ans: {ans}")
    nbrs = get_nbrs(G, pos)
    for i,nbr in enumerate(nbrs):
        print(f"{i:2d} {nbr}")
    pic = input("pick nbr #: ")
    pic = int(pic)
    pos = nbrs[pic]
    print(f" -> new_pos = {pos}")
    r = pos[1]
    c = pos[2]
    val = G[r][c]
    ans += val


