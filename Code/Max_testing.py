from network_editing_operations import *
from graph_functionality import *
from simplifying_operations import beam_search, greedy_search
from bmg_fun import compute_bmg
import networkx as nx
from copy import deepcopy
import BICcherry
from bmg_Tony import bmg


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

"""
# test graph, deprecated
G = nx.DiGraph()
G.add_nodes_from(['x', 'y1', 'y2', 'y3', "roh", "v"])
G.add_edges_from([("roh", "v"), ("roh", "y2"),("roh", "y3"), ("v", "x"), ("v", "y1")])
sigma = {"x" : "r", "y1":"g", "y2":"g", "y3":"g"}

BIC_NW = nx.DiGraph()
inverse_edges = ([("x", "pxy1"), ("x", "pxy2"), ("x", "pxy3"), ("y1", "pxy1"), ("y2", "pxy2"), ("y3", "pxy3"),
                       ("pxy1", "roh"), ("pxy2", "roh"), ("pxy3", "roh"),
                       ("x", "qxy1"), ("x", "qxy2"), ("y1", "qxy1"), ("y1", "qxy2"),
                       ("qxy1", "pxy2"), ("qxy2", "pxy3")])
BIC_NW.add_edges_from((value, key) for (key, value) in inverse_edges)"""

def generate_tree(seed = 3):
    import numpy as np
    import asymmetree.treeevolve as te
    from bmg_fun import convert_to_nx
    import insert_hybrid

    random.seed(seed)
    np.random.seed(seed)

    # species tree
    S = te.species_tree_n_age(
        3, 0.5, contraction_probability=0.0, contraction_proportion=0.2, contraction_bias="exponential"
    )
    # gene tree
    T = te.dated_gene_tree(
        S, dupl_rate=0.75, loss_rate=0, hgt_rate=0.2, gc_rate=0.2, prohibit_extinction="per_species", dupl_polytomy=0.5
    )
    # prune all loss branches and the planted root
    observable_gene_tree = te.prune_losses(T)

    tree_to_nx = convert_to_nx(observable_gene_tree)
    #return insert_hybrid.insertHybrid(tree_to_nx, 3)

    return tree_to_nx

G = generate_tree(3) #3 and 1 produce assertion errors

from bmg_Tony import bmg
bic_cherry = BICcherry.BICcherry(bmg(G, mode="weak"))

#display_multiple_trees([G, bic_cherry] + beam_search(bic_cherry, max_number_of_steps=10, top_n=5))
display_multiple_trees([G, bic_cherry] + [greedy_search(bic_cherry, max_number_of_steps=50)])


