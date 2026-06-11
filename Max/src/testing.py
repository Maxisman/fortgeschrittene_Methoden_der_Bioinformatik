from network_editing_operations import *
from graph_functionality import *
from simplifying_operations import *
import networkx as nx
from copy import deepcopy


"""
#test code from testing network editing operations
if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node("b1",color="b")
    G.add_node("b2",color="b")
    G.add_node("c1",color="r")
    G.add_node("c2",color="r")
    G.add_node("a1",color="g")
    G.add_edges_from([("roh", "u"), ("u", "a1"), ("u", "w"), ("w", "b1"), ("w", "c1"), ("roh", "v"), ("v", "b2"), ("v", "c2"), ("u", "c1")])
    sigma = {"a1" : "g", "b1":"b", "b2":"b", "c1":"r", "c2":"r"}
    #redundant nodes x and y
    G.add_edges_from([("roh", "x"), ("x", "b2"), ("x", "c2")])
    G.add_edges_from([("roh", "y"), ("y", "b2"), ("y", "c2")])
    original = G

    # basic operations
    # G = deepcopy(original)
    # pull_down(G, "a1", "u", "w")
    # H = deepcopy(original)
    # pull_up(H, "b1", "w", "u")
    # I = deepcopy(original)
    # remove_redundant_vertices(I)
    # print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(G, "roh", sigma)))
    # display_multiple_trees([original,H, G, I], sigma)

    # reach tree
    # G = deepcopy(original)
    # remove_redundant_vertices(G)
    # H = deepcopy(G)
    # pull_down(H, "c1", "u", "w")
    # print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(H, "roh", sigma)))
    # display_multiple_trees([original, G, H], sigma)

    # break bmg
    G = deepcopy(original)
    pull_up(G, "a1", "u", "roh")
    #pull_down(G, "w", "u", "c1")
    print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(G, "roh", sigma)))
    display_multiple_trees([original, G], sigma)
"""

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
neighborhood = generate_editing_neighborhood(G)
#pull_up(modified, "y3", "pxy3", "roh")
#pull_up(modified, "x", "pxy3", "roh")

for G in neighborhood:
    remove_non_informative_nodes(G)

remove_equal_graphs(neighborhood)

neighborhood = beam_search_step([G], sigma, compute_tree_bmg, step_size= 2) # this has failed for step_size=3 but I believe this is due to an error in my graph_functionality/lca function which will be dropped anyway so I didnt fix it
display_multiple_trees([G] + neighborhood, sigma)

# debug display_multiple_trees function: works not with only one graph
# van neumann entropie