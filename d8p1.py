import pydot

def write_graph(nodes):
    graph = pydot.Dot("my_graph", graph_type="digraph")

    for node in nodes.keys():
        color="lightgrey"
        if node == "AAA":
            color="green"
        elif node == "ZZZ":
            color="red"
        attrs = {
            "style": "filled",
            "fillcolor" : color,
        }
        n = pydot.Node(node, label=node,**attrs )
        graph.add_node(n)

    for k,v in nodes.items():
        graph.add_edge(pydot.Edge(k, v[0], color="blue"))
        graph.add_edge(pydot.Edge(k, v[1], color="red"))

    graph.write_png("output.png")

def get_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    
    lines = [line.strip('\n') for line in lines]
    Is = lines[0]
    
    lines = lines[2:]

    nodes = {}
    for line in lines:
        node,rest = line.split(' = (')
        rest = rest.removesuffix(')')
        l,r = rest.split(',')
        l = l.strip()
        r = r.strip()
        nodes[node] = (l,r)

    return Is, nodes


class Guy:
    def __init__(self, Is, nodes, pos="AAA"):
        self.Is = Is
        self.nodes = nodes
        self.pos = pos
        self.i = 0
        self.steps = 0
    def get_state(self):
        i = self.i
        pos = self.pos
        return (i, pos)
    def step(self):
        instr = self.Is[self.i]
        L,R = self.nodes[self.pos]
        if instr == "L":
            self.pos = L
        else:
            self.pos = R
        self.i += 1
        if self.i >= len(self.Is):
            self.i = 0
        self.steps += 1



fname = "in_08.txt"
#fname = "ex_08.txt"
#fname = "ex_08a.txt"
Is, nodes = get_input(fname)
me = Guy(Is, nodes)

pos = me.pos
print(f"pos: {pos}")

while pos != "ZZZ":
    me.step()
    print(f"state: {me.get_state()} steps: {me.steps}")
    pos = me.pos
#write_graph(nodes)
    