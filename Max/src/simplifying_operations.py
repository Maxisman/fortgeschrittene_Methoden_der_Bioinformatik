from network_editing_operations import *
from graph_functionality import graphs_equal
import networkx as nx
from copy import deepcopy
from _collections_abc import Callable
import itertools
import heapq

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

    for G in neighborhood:
        remove_non_informative_nodes(G)

    return neighborhood

def remove_equal_graphs(neighborhood: list[nx.DiGraph]):
    """
    Removes all duplicate graphs from a list of graphs. This only works if duplicates have the same node labelings.

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

def compute_tree_likeness(G):
    """
    computes the tree likeness score as negative (number of edges - 2* number of nodes). The higher the score the more tree-like

    The idea behind that is that an ideal tree has as few edges as possible (especially no hybrid edges). However each node has at least two edges so we do not want to discourage creating more nodes (for now)
    """
    return -( len(G.edges()) - 2 * len(G.nodes()))

def helper_tree_likeness(G, coloring, bmg, bmg_function, tree_likeness_function, NEGATIVE_INFINITY):
    """
    Helper for beam_search(). Returns a score of tree likeness or NEGATIVE_INFINITY if the network's bmg is wrong
    """
    if not graphs_equal(bmg, bmg_function(G, coloring)):
        return (NEGATIVE_INFINITY)
    else:
        return (tree_likeness_function(G))


def beam_search_step(graphs:list[nx.DiGraph], coloring:dict, bmg_function:Callable[[nx.DiGraph, dict], nx.DiGraph], top_n:int = 10, step_size:int = 3, tree_likeness_function:Callable[[nx.DiGraph], int] = compute_tree_likeness): #TODO: add Julias bmg function as default
    """
    Tries to make a set of networks more tree-like while conserving the network's best match graph. This is achieved by calculating the neighborhood of a graph for up to step_size steps and then taking the top n graphs according to the tree likeness.

    Parameters
    ----------
    graphs: list[networkx.DiGraph]
        number of graphs that will be used as a base for improvement
    coloring:dict
        leaf coloring neccessary for bmg function
    bmg_function: function
        function for calculating a best match graph from a network
    top_n: int
        number of graphs with the best scores that will be returned
    step_size: int
        maximum number of editing operations before the bmg and loss will be evaluated. Higher step size allows better operations but decreases performance exponentially.
    loss_function: function
        calculates the loss for tree likeness of a network. Higher values mean more tree-like
    """

    NEGATIVE_INFINITY = -1000000
    bmg = bmg_function(graphs[0], coloring)

    for step in range(step_size):
        neighborhood = []
        for G in graphs:
            neighborhood += generate_editing_neighborhood(G)
        graphs = graphs + neighborhood
        remove_equal_graphs(graphs) #TODO: make that more efficient

    scored_graphs = ((helper_tree_likeness(G, coloring, bmg, bmg_function, tree_likeness_function, NEGATIVE_INFINITY), G) for G in graphs)
    valid_graphs = ((score, G) for score, G in scored_graphs if score > NEGATIVE_INFINITY)
    top_graphs = heapq.nlargest(top_n, valid_graphs, key = lambda x : x[0])

    return [G for score, G in top_graphs]

    #new_batch = heapq.nlargest(top_n, graphs, key= (lambda G : helper_tree_likeness(G, bmg, bmg_function, tree_likeness_function, NEGATIVE_INFINITY)))