from queue import Queue

def get_ij(id, NJ):
    i = id // NJ
    j = id % NJ
    return (i,j)

def get_id(i,j, NJ):
    id = i * NJ + j

    return id

def get_ord(char):
    if char == 'S':
        char = 'a'
    elif char == 'E':
        char = 'z'
    return ord(char) - 97

class Graph:
    def __init__(self, num_of_nodes, directed=True):
       self.m_num_of_nodes = num_of_nodes
       self.m_nodes = range(self.m_num_of_nodes)

       self.m_directed = directed

       # adjacency list as map from node to adjacent nodes
       self.m_adj_list = {node: set() for node in self.m_nodes}
    
    def add_edge(self, node1, node2, weight=1):
        self.m_adj_list[node1].add((node2, weight))

        if not self.m_directed:
            self.m_adj_list[node2].add((node1, weight))
    
    def print_adj_list(self):
        for key in self.m_adj_list.keys():
            print('node', key, ": ", self.m_adj_list[key])
    
    def bfs(self, start_node, target_node):
        visited = set()
        q = Queue()

        q.put(start_node)
        visited.add(start_node)

        parent = dict()
        parent[start_node] = None

        path_found = False
        while not q.empty():
            current_node = q.get()
            if current_node == target_node:
                path_found = True
                break
            
            for (next_node, weight) in self.m_adj_list[current_node]:
                if next_node not in visited:
                    q.put(next_node)
                    parent[next_node] = current_node
                    visited.add(next_node)
        
        path = []
        if path_found:
            path.append(target_node)
            while parent[target_node] is not None:
                path.append(parent[target_node])
                target_node = parent[target_node]

            path.reverse()
        return path

graph = Graph(6, directed=True)

#      N  S  E  W
di = [-1, 1, 0, 0]
dj = [ 0, 0, 1,-1]

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
            
def print_grid(G, xi=-1, xj=-1):
    print('   0  1  2  3  4  5  6  7')
    for i in range(len(G)):
        print(f'{i} ',end='')
        for j in range(len(G[i])):
            print(f'{G[i][j]:>2s}', end=' ')
        print()

def print_grid_as_nums(G, xi=-1, xj=-1):
    #print('  0 1 2 3 4 5 6 7')
    print('_________________________')
    for i in range(len(G)):
        for j in range(len(G[i])):
            i_num = get_ord(G[i][j])
            if i == xi and j == xj:
                char = '_x'
                print(f'{char:2s}', end=' ')
            else:
                print(f'{i_num:2d}', end=' ')
        print()

def find_char(G, char):
    i = 0
    j = 0
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] == char:
                return i,j
    return i,j

def build_adj_list(graph:Graph, grid:list[list[str]]):
    NI = len(grid)
    NJ = len(grid[0])

    # look at each node: add valid edges
    for i in range(NI):
        for j in range(NJ):
            i_node_id = get_id(i,j,NJ)
            i_num = get_ord(grid[i][j])
            # get neighbors
            for k in range(4):
                ni = i + di[k]
                nj = j + dj[k]
                if ni < 0 or ni >= NI: continue
                if nj < 0 or nj >= NJ: continue
                o_node_id = get_id(ni,nj,NJ)
                o_num = get_ord(grid[ni][nj])

                # add other if we can reach it
                if o_num <= i_num + 1:
                    graph.add_edge(i_node_id, o_node_id)
    
    
def find_node_id( grid:list[list[str]], the_char):
    NI = len(grid)
    NJ = len(grid[0])

    # start node has char = 'S'
    # end   node has char = 'E'

    # look at each node: add valid edges
    for i in range(NI):
        for j in range(NJ):
            i_node_id = get_id(i,j,NJ)
            i_char = grid[i][j]
            if i_char == the_char:
                return i_node_id
    return -1


lines = get_lines('input.txt')
#lines = get_lines('example.txt')
grid = make_grid(lines)
NI = len(grid)
NJ = len(grid[0])

graph = Graph(NI*NJ, directed=True)

build_adj_list(graph, grid)

#print('-- ADJ LIST -- ')
#graph.print_adj_list()
#print('-- ADJ LIST -- ')

def get_all_a_node_ids(grid):
    NI = len(grid)
    NJ = len(grid[0])

    # looking for all 'a's
    a_node_list = []

    # look at each node: add valid edges
    for i in range(NI):
        for j in range(NJ):
            i_node_id = get_id(i,j,NJ)
            i_char = grid[i][j]
            if i_char == 'a' or i_char == 'S':
                a_node_list.append(i_node_id)

    return a_node_list

# PART 1
#node_s = find_node_id(grid, 'S')
#node_e = find_node_id(grid, 'E')
#print(f'start w/ id = {node_s}')
#print(f'end   w/ id = {node_e}')
#
#path = graph.bfs(node_s,node_e)
#
#print(path)
#print('len = ', len(path)-1)

# PART 2
node_e = find_node_id(grid, 'E')
a_node_list = get_all_a_node_ids(grid)

path_steps = []

for inode in a_node_list:
    path = graph.bfs(inode, node_e)
    i,j = get_ij(inode, len(grid[0]))
    steps = len(path) - 1
    if steps >= 0:
        path_str=f'steps = {steps:>2d} for node {inode:>4d} at {i:>2d},{j:>2d}'
        path_steps.append((steps, path_str))

ps = sorted(path_steps, key= lambda x: x[0], reverse=True)

for steps, str in ps:
    print(str)







#for pos in path:
#    i,j = get_ij(pos, len(grid[0]))
#    print_grid_as_nums(grid, i, j)
#    x = input()
