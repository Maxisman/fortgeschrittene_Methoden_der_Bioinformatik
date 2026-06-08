from network_editing_operations import *
from graph_functionality import *
from simplifying_operations import *
import networkx as nx
from copy import deepcopy

G = nx.DiGraph()
G.add_nodes_from(['x', 'y1', 'y2', 'y3', "roh", "v"])
G.add_edges_from([("roh", "v"), ("roh", "y2"),("roh", "y3"), ("v", "x"), ("v", "y1")])
sigma = {"x" : "r", "y1":"g", "y2":"g", "y3":"g"}

BIC_NW = nx.DiGraph()
inverse_edges = ([("x", "pxy1"), ("x", "pxy2"), ("x", "pxy3"), ("y1", "pxy1"), ("y2", "pxy2"), ("y3", "pxy3"),
                       ("pxy1", "roh"), ("pxy2", "roh"), ("pxy3", "roh"),
                       ("x", "qxy1"), ("x", "qxy2"), ("y1", "qxy1"), ("y1", "qxy2"),
                       ("qxy1", "pxy2"), ("qxy2", "pxy3")])
BIC_NW.add_edges_from((value, key) for (key, value) in inverse_edges)

modified = deepcopy(BIC_NW)
generate_neighborhood(G)
#pull_up(modified, "y3", "pxy3", "roh")
#pull_up(modified, "x", "pxy3", "roh")

display_multiple_trees([G, BIC_NW, modified], sigma) 
# debug display_multiple_trees function: works not with only one graph
# debug bmg function
# van neumann entropie