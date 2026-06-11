from network_editing_operations import *
from graph_functionality import graphs_equal
import networkx as nx
from copy import deepcopy
import itertools

"""
    This script provides methods to simplify a graph network
"""

def generate_editing_neighborhood(G: nx.DiGraph):
    """ Generates neighborhood of graphs that can be achieved by one graph edit operation. In each tree redundant and non-informative nodes will be removed.

    Parameters
    ----------
    G: nx.Digraph
        Graph that should be edited

    Returns
    -------
    neighborhood: list(nx.DiGraph)
        list of graphs that can be reached from G in one edit operation
    """

    # by default remove redundant vertices beforehand (might be changed later)
    remove_non_informative_nodes(G)
    remove_redundant_vertices(G)
    neighborhood = []

    # pull up moves
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

def remove_equal_graphs(neighborhood: list[nx.DiGraph]):
    """
    Removes all duplicate graphs from a list of graphs

    This limits the number of graphs that need to be examined and facilitates beam search
    """
    removal = []
    for G in neighborhood:
        if G in removal:
            continue
        for H in neighborhood:
            if H == G:
                continue
            if graphs_equal(G, H):
                removal.append(H)
    
    for G in removal:
        neighborhood.remove(G)

    return neighborhood
