from network_editing_operations import *
from graph_functionality import *
from simplifying_operations import greedy_search
import networkx as nx
import BICcherry
from bmg_Tony import bmg
from copy import deepcopy
import numpy as np
import asymmetree.treeevolve as te
from bmg_fun import convert_to_nx


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

for seed in range(50):
    G, colors = generate_tree(seed)
    bic_cherry = BICcherry.BICcherry(bmg(G, mode="weak"))

    if nx.utils.graphs_equal(bmg(G), bmg(bic_cherry)):
        original_bic = deepcopy(bic_cherry)
        improved_network = greedy_search(bic_cherry, max_number_of_steps=50)
        assert(nx.utils.graphs_equal(bmg(original_bic), bmg(improved_network)))
        print(f"seed is {seed}")
        display_multiple_trees([G, original_bic, improved_network], colors)
    