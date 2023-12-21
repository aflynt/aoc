from lib import *
import pydot
from math import lcm

fname = ["ex1.txt", "ex2.txt", "in.txt"][-1]
mstrs = open(fname).read().strip('\n').split('\n')
ms = get_modules(mstrs)

nlo = 0
nhi = 0
bpress = 1
multiples = []

while len(multiples) < 4:
    x,lopp,hipp = get_pulses(bpress, ms)
    if x > 0:
        multiples.append(x)
    nlo += lopp
    nhi += hipp
    if bpress == 1000:
        ans = nlo*nhi
        print(f"p1: {ans}")
    bpress += 1

#print(multiples)
a2 = lcm(*multiples)
print(f"p2: {a2}")

#graph = pydot.Dot("my_graph", graph_type="digraph")
#
## add nodes
#for mname, m in ms.items():
#    label_str = m.__str__()
#    if mname == "output":
#        graph.add_node(pydot.Node(mname, shape="circle", style="filled", fillcolor="red", margin="0.1"))
#    elif mname == "button":
#        graph.add_node(pydot.Node(mname, shape="circle", style="filled", fillcolor="blue", margin="0.1"))
#    elif "&" in label_str:
#        graph.add_node(pydot.Node(mname , shape="circle", style="filled", fillcolor="grey", label=label_str))
#    elif "%" in label_str:
#        graph.add_node(pydot.Node(mname , shape="circle", style="filled", fillcolor="cyan", label=label_str))
#    else:
#        graph.add_node(pydot.Node(mname , shape="circle", style="filled", fillcolor="white", label=label_str))
#
## add edges
#for mname, m in ms.items():
#    label_str = m.__str__()
#    outputs = m.outputs
#    if mname in ["output", "broadcaster", "button"]:
#        c = "black"
#    elif "&" in label_str:
#        c = "red"
#    else:
#        c = "blue"
#    for output in outputs:
#        graph.add_edge(pydot.Edge(mname, output, color=c))

#output_raw_dot = graph.to_string()
#x = graph.write()
#graph.write_raw("output_graphviz.dot")
#graph.write_png("output.png")


#with open("res.dat", "w") as f:
#    for k,v in ms.items():
#        f.write(f"{k:11s} IN:{v.inputs} OUT: {v.outputs}\n")