from lib import *
import matplotlib.pyplot as plt
import pydot


fname = ["ex1.txt", "ex2.txt", "in.txt"][-1]
mstrs = open(fname).read().strip('\n').split('\n')
ms = get_modules(mstrs)

graph = pydot.Dot("my_graph", graph_type="digraph")

# add nodes
for mname, m in ms.items():
    label_str = m.__str__()
    if mname == "output":
        graph.add_node(pydot.Node(mname, shape="circle", style="filled", fillcolor="red", margin="0.1"))
    elif mname == "button":
        graph.add_node(pydot.Node(mname, shape="circle", style="filled", fillcolor="blue", margin="0.1"))
    elif "&" in label_str:
        graph.add_node(pydot.Node(mname , shape="circle", style="filled", fillcolor="grey", label=label_str))
    elif "%" in label_str:
        graph.add_node(pydot.Node(mname , shape="circle", style="filled", fillcolor="cyan", label=label_str))
    else:
        graph.add_node(pydot.Node(mname , shape="circle", style="filled", fillcolor="white", label=label_str))

# add edges
for mname, m in ms.items():
    label_str = m.__str__()
    outputs = m.outputs
    if mname in ["output", "broadcaster", "button"]:
        c = "black"
    elif "&" in label_str:
        c = "red"
    else:
        c = "blue"
    for output in outputs:
        graph.add_edge(pydot.Edge(mname, output, color=c))

output_raw_dot = graph.to_string()
#x = graph.write()
graph.write_raw("output_graphviz.dot")
#graph.write_png("output.png")

"""
def get_states(ms: dict[str, Module]) -> list[int]:
    states = []
    for mname, m in ms.items():
        state = m.get_state_list()
        #print(f"{mname}: {m} {state}")
        states += state
    return states



nhi = 0

bpress = 1

bps = []
ss = []

"""
with open("res.dat", "w") as f:
    for k,v in ms.items():
        f.write(f"{k:11s} IN:{v.inputs} OUT: {v.outputs}\n")


#    while bpress < 100001:
#        ms,lopp,hipp = get_pulses(ms)
#        nlo += lopp
#        nhi += hipp
#        #print(f"btn press: {bpress} lo: {lopp} hi: {hipp} nlo: {nlo}, nhi: {nhi}")
#        states = get_states(ms)
#        #print(f"{bpress:5d} {sum(states)}")
#        bps.append(bpress)
#        ss.append(sum(states))
#        #f.write(f"{bpress:5d} {sum(states)}\n")
#        bpress += 1
#        #x = input()


#npress = 1000
#nlo = lopp * npress
#nhi = hipp * npress
#ans = nlo*nhi

#print(f"nlo: {nlo}, nhi: {nhi}, ans: {ans}")