from network_editing_operations import *
import networkx as nx
from copy import deepcopy

def generate_neighborhood(G: nx.DiGraph):
    # by default remove redundant vertices beforehand (might be changed later)
    remove_redundant_vertices(G)
    neighborhood = []

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