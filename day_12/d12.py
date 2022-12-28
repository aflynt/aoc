
fname = 'example.txt'

#     N   S   E   W
dr = [-1, 1 , 0 ,  0]
dc = [ 0, 0 , 1 , -1]

class vertex:
    def __init__(self, i,j, value, NI=5, NJ=8):
        self.i = i
        self.j = j
        self.NI = NI
        self.NJ = NJ
        self.value = value


def get_lines(fname):
    lines = []

    with open(fname, 'r') as f:
        lines = f.readlines()
    
    lines = [ line.strip() for line in lines]
    return lines

def make_grid(lines:list[str]):

    rows = []
    for line in lines:
        rowvals = []
        for char in line:
            rowvals.append(char)
        rows.append(rowvals)

    return rows
            
def print_grid(G):
    print('  0 1 2 3 4 5 6 7')
    for i in range(len(G)):
        print(f'{i} ',end='')
        for j in range(len(G[i])):
            print(G[i][j], end=' ')
        print()

def find_char(G, char):
    i = 0
    j = 0
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] == char:
                return i,j
    return i,j

def make_distance_grid( G, si, sj, val=1e6):

    dg = []
    
    #initialize all values to max value
    for i in range(len(G)):
        dgrowvals = []
        for j in range(len(G[i])):
            dgrowvals.append(int(val))
        dg.append(dgrowvals)

    dg[si][sj] = 0

    return dg
    
def update_neighbor_distances(D,G,rs,cs):
    NR = len(G)
    NC = len(G[0])

    for i in range(4):
        r = rs + dr[i]
        c = cs + dc[i]

        if r < 0 or r >= NR: continue
        if c < 0 or c >= NC: continue
        if G[r][c] - G[rs][cs]> 2: continue

    

#####################################
lines = get_lines(fname)
G = make_grid(lines)
NI = len(G)
NJ = len(G[0])

print_grid(G)

# find start and end
si,sj = find_char(G, 'S')
ei,ej = find_char(G, 'E')

# set sptSet is empy
sptSet = set()

# distances assigned to vertices are {0, INF}
D = make_distance_grid(G, si, sj)
print_grid(D)

# now pick vertex with min dist value 'si, sj'. include it in the set.
sptSet.add((si,sj))

# After including 0 to sptSet, update distance values of its adjacent vertices. 
update_neighbor_distances(D,G,si,sj)

print(f'start at i,j = {si},{sj}')
print(f'end   at i,j = {ei},{ej}')


