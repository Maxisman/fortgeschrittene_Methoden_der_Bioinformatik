from network_editing_operations import *
from graph_functionality import *
from simplifying_operations import greedy_search
import networkx as nx
import BICcherryRestrict
from bmg_Tony import bmg
from copy import deepcopy
import numpy as np
import asymmetree.treeevolve as te
from bmg_fun import convert_to_nx
from EffRes import path_minus_resistance
import bmg_fun
from lrt_fun import lrt_from_bmg
from BICcherry_reverse import BICcherry_reverse


def generate_tree(seed = 3):
    random.seed(seed)
    np.random.seed(seed)

    # species tree
    S = te.species_tree_n_age(
        3, 0.59, contraction_probability=0.0, contraction_proportion=0.2, contraction_bias="exponential"
    )
    # gene tree
    T = te.dated_gene_tree(
        S, dupl_rate=0.75, loss_rate=0, hgt_rate=0.2, gc_rate=0.2, prohibit_extinction="per_species", dupl_polytomy=0.5
    )
    # prune all loss branches and the planted root
    observable_gene_tree = te.prune_losses(T)

    tree_to_nx = convert_to_nx(observable_gene_tree)

    #color stuff
    from asymmetree.visualization.tree_vis import assign_colors
    species_colors, gene_colors = assign_colors(S, observable_gene_tree)
    gene_colors_str = {str(k): v for k, v in gene_colors.items()}

    return tree_to_nx, gene_colors_str

def return_example_tree():
    lrt = nx.DiGraph()
    lrt.add_nodes_from([("4", {"color": "red"}), ("5", {"color": "blue"}), ("19-20", {"color": "orange"}), ("15", {"color": "yellow"}), ("13", {"color": "orange"}), ("14", {"color": "yellow"}), ("21-22", {"color": "orange"}), ("11", {"color": "yellow"})])
    lrt.add_edges_from([("roh", "4"), ("roh", "5"), ("roh", "inner1"), ("roh", "inner2"), ("roh", "inner3"),
                        ("inner1", "19-20"), ("inner1", "15"),
                        ("inner2", "13"), ("inner2", "14"),
                        ("inner3", "21-22"), ("inner3", "11")])
    color_dict = {
        "4" : "red",
        "5" : "blue",
        "19-20" : "orange",
        "15" : "yellow",
        "13" : "orange",
        "14" : "yellow",
        "21-22" : "orange",
        "11" : "yellow"
    }
    return lrt, color_dict

def return_example_tree2():
    lrt = nx.DiGraph()
    lrt.add_nodes_from([("14", {"color": "blue"}), ("15", {"color": "red"}), ("20-21", {"color": "blue"}), 
                        ("7", {"color": "orange"}), ("16", {"color": "purple"}), ("17", {"color": "green"}), 
                        ("9", {"color": "orange"}), ("23", {"color": "orange"}),
                        ("22", {"color": "red"}), ("19", {"color": "yellow"}), ("24-25", {"color": "yellow"})])
    lrt.add_edges_from([('inner 0', 'inner 1'), ('inner 0', 'inner 5'), ('inner 1', 'inner 2'), ('inner 1', 'inner 4'), ('inner 2', '7'), ('inner 2', '20-21'), ('inner 2', 'inner 3'), ('inner 3', '15'), ('inner 3', '14'), ('inner 4', '16'), ('inner 4', '9'), ('inner 4', '17'), ('inner 5', '24-25'), ('inner 5', 'inner 6'), ('inner 6', '23'), ('inner 6', '22'), ('inner 6', '19')]
)
    lrt.remove_nodes_from(["16", "17"])
    color_dict = {
        "14" : "blue",
        "15" : "red",
        "20-21" : "blue",
        "7" : "orange",
        "16" : "purple",
        "17" : "green",
        "9" : "orange",
        "23" : "orange",
        "22" : "red",
        "19" : "yellow",
        "24-25" : "yellow"}
    return lrt, color_dict

i = 0
for seed in range(5000):
    #G, colors = generate_tree(seed)
    G, colors = return_example_tree2()
    # thin_BMG, thin_gene_colors = bmg_fun.thinness_graph(bmg(G, mode = "weak"), colors)
    # lrt = lrt_from_bmg(thin_BMG)
    lrt = lrt_from_bmg(bmg(G, mode="weak"))
    thin_BMG = bmg(G, mode="weak")
    thin_gene_colors = colors

    #bic_cherry = BICcherryRestrict.BICcherryRestrict(thin_BMG)
    bic_cherry = BICcherry_reverse(thin_BMG, simplify=True)

    if nx.utils.graphs_equal(bmg(G, "weak"), bmg(bic_cherry, "weak")):
        improved_network = greedy_search(bic_cherry, max_number_of_steps=150, tree_likeness_function = compute_tree_likeness)
        assert(nx.utils.graphs_equal(bmg(bic_cherry), bmg(improved_network)))
        print(f"The seed is: {seed}")
        i += 1
        if compute_tree_likeness(lrt) != compute_tree_likeness(improved_network):
            display_multiple_graphs([G, lrt, bic_cherry, improved_network], thin_gene_colors | colors)
print(i)


