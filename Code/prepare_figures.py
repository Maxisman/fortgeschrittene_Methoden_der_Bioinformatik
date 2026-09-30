from network_editing_operations import *
import networkx as nx
from graph_functionality import display_multiple_graphs
from copy import deepcopy


G = nx.DiGraph()
G.add_nodes_from([("a1", {"color": "red"}), ("b1", {"color": "blue"}), ("c1", {"color": "orange"}), ("b2", {"color": "blue"}), ("c2", {"color": "orange"})])
G.add_edges_from([("roh", "u"), ("roh", "v"), ("roh", "x"), ("roh", "y"), 
            ("v", "c2"), ("x", "c2"), ("y", "c2"), ("v", "b2"), ("x", "b2"), ("y", "b2"), 
            ("u", "w"), 
            ("w", "c1"), ("w", "b1"), ("u", "c1"), ("u", "a1")])
color_dict = {
    "a1" : "red",
    "b1" : "blue",
    "b2" : "blue",
    "c1" : "orange",
    "c2" : "orange"
}

H = deepcopy(G)
pull_up(H, "b1", "w", "u")
I = deepcopy(G)
pull_up(I, "c1", "w", "u")
J = deepcopy(G)
pull_up(J, "a1", "u", "roh")


labels = ["original graph", "pull up on b1", "pull up on c1", "pull up on a1 changes the bmg"]
#display_multiple_graphs([G, H, I, J], color_dict, labels= labels)


H = deepcopy(G)
pull_down(H, "a1", "u", "w")
I = deepcopy(G)
pull_down(I, "c1", "u", "w")
J = deepcopy(G)
pull_down(J, "v", "roh", "u")

labels = ["original graph", "pulling down (u, a1)", "pulling down (u, c1)", "pulling down (v, roh) changes the bmg"]
#display_multiple_graphs([G, H, I, J], color_dict, labels= labels)

H = deepcopy(G)
remove_redundant_vertices(H)
#display_multiple_graphs([G, H], color_dict, labels = ["original graph", "removed redundant nodes"])

H = deepcopy(G)
pull_up(H, "c1", "w", "u")
I = deepcopy(H)
remove_non_informative_nodes(I)

#display_multiple_graphs([H, I], color_dict, labels = ["original graph (c1 pulled up)", "removed non-informative node"])



# A = nx.DiGraph()
# A.add_nodes_from([("8", {"color": "green"}), ("9", {"color": "green"}), ("7", {"color": "orange"}), ("3", {"color": "blue"}), ("6", {"color": "orange"})])
# A.add_edges_from([("roh", "6"), ("roh", "7"), ("roh", "3"), ("roh", "p_8_9"), ("p_8_9", "8"), ("p_8_9", "9"), ])
# color_dict = {
#     "8" : "green",
#     "9" : "green",
#     "3" : "blue",
#     "6" : "orange",
#     "7" : "orange"
# }
# B = deepcopy(A)
# pull_up(B, "8", "p_8_9", "roh")
# C = deepcopy(B)
# pull_up(C, "9", "p_8_9", "roh")
# C.remove_node("p_8_9")

# display_multiple_graphs([A, B, C], color_dict, labels = ["original graph", "pull up action changes bmg", "contracting edge"])

H = deepcopy(G)
pull_up(H, "b1", "w", "u")
I = deepcopy(G)
pull_up(I, "c1", "w", "u")
pull_up(I, "b1", "w", "u")
I.remove_node("w")
J = deepcopy(G)
pull_down(J, "a1", "u", "w")
J.remove_node("v")

#display_multiple_graphs([G, H, I, J], color_dict)

K = deepcopy(G)
remove_redundant_vertices(K)
L = deepcopy(K)
pull_up(L, "c1", "w", "u")
#display_multiple_graphs([G,K,L], color_dict)

mode = 'weak'

Netz = nx.DiGraph()
Netz.add_node('rho')
Netz.add_node('1')
Netz.add_node('2')
Netz.add_node('3')
Netz.add_node('x1', color = 'red')
Netz.add_node('x2', color = 'red')
Netz.add_node('x3', color = 'red')
Netz.add_node('y1', color = 'blue')
Netz.add_node('y2', color = 'blue')
Netz.add_node('y3', color = 'blue')

Netz.add_edges_from([('rho','1'),('rho','2')])
Netz.add_edges_from([('1','3'),('1','x2'),('1','y3')])
Netz.add_edges_from([('2','3'),('2','y2'),('2','x3')])
Netz.add_edges_from([('3','x1'),('3','y1')])

Netz.remove_nodes_from(["2", "y2", "x3"])

from bmg_Tony import bmg
from BICcherry_reverse import BICcherry_reverse
BMG = bmg(Netz, mode)
RBC_pre = BICcherry_reverse(BMG)
color_dict = {
    "x1" : "red",
    "x2" : "red",
    "x3" : "red",
    "y1" : "blue",
    "y2" : "blue",
    "y3" : "blue",
}

improved = RBC_pre.copy()
improved.remove_nodes_from(["q_x2_y1"])
improved.add_edge("q_y3_x1", "x2")
improved2 = improved.copy()
improved2.remove_node("p_x2_y3")

display_multiple_graphs([RBC_pre, improved, improved2], color_dict)