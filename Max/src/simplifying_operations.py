from network_editing_operations import *
import networkx as nx
from copy import deepcopy
import itertools

def generate_neighborhood(G: nx.DiGraph):
    # by default remove redundant vertices beforehand (might be changed later)
    remove_redundant_vertices(G)
    neighborhood = []

    # pull ov moves
    pull_up_candidates = []
    for grandparent in G.nodes:
        parents = G.successors(grandparent)
        for parent in parents:
            children = G.successors(parent)
            pull_up_candidates += [(grandparent, parent, child) for child in children]
    
    for (grandparent, parent, child) in pull_up_candidates:
        H = deepcopy(G)
        pull_up(H, child, parent, grandparent)
        neighborhood.append(H)

    # pull down moves
    pull_down_candidates = []
    for parent in G.nodes:
        if G.out_degree(parent) <= 1:
            continue
        pull_down_candidates += [(c1, parent, c2) for c1, c2 in itertools.permutations(G.successors(parent), 2)]

    for (child, parent, new_parent) in pull_down_candidates:
        H = deepcopy(G)
        pull_down(H, child, parent, new_parent)
        neighborhood.append(H)

    return neighborhood

# remove unneccessary nodes a -> unneccessary -> b