from network_editing_operations import *
from graph_functionality import compute_tree_likeness, extended_tree_likeness
from graph_functionality import display_multiple_trees
from bmg_Tony import bmg
import networkx as nx
from copy import deepcopy
from _collections_abc import Callable
import itertools
import heapq

"""
    This script provides methods to simplify a graph network
"""

### BEAM SEARCH

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
            if nx.utils.graphs_equal(G, H):
                removal.append(H)
    
    for G in removal:
        neighborhood.remove(G)

    return neighborhood

def beam_search_step(networks:list[nx.DiGraph], 
                     bmg_function:Callable[[nx.DiGraph, str], nx.DiGraph] = bmg, 
                     top_n:int = 10, 
                     step_size:int = 1, 
                     tree_likeness_function:Callable[[nx.DiGraph], int] = compute_tree_likeness, 
                     mode:str="weak"):
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
    mode: str
        either strong or weak, selects best match definition
    """

    NEGATIVE_INFINITY = -1000000
    bmg = bmg_function(networks[0], mode)

    for step in range(step_size):
        neighborhood = []
        for G in networks:
            neighborhood = neighborhood + generate_editing_neighborhood(G)
        networks = networks + neighborhood
        remove_equal_graphs(networks) #TODO: make that more efficient
        print(f"Finished step {step + 1}/{step_size}")


    scored_graphs = [(extended_tree_likeness(G, bmg, bmg_function, tree_likeness_function, NEGATIVE_INFINITY, mode), G) for G in networks]
    valid_graphs = [(score, G) for score, G in scored_graphs if score > NEGATIVE_INFINITY]
    top_graphs = heapq.nlargest(top_n, valid_graphs, key = lambda x : x[0])

    return [G for score, G in top_graphs]

    #new_batch = heapq.nlargest(top_n, graphs, key= (lambda G : helper_tree_likeness(G, bmg, bmg_function, tree_likeness_function, NEGATIVE_INFINITY)))

def beam_search(network:nx.DiGraph,
                max_number_of_steps:int = 100,
                bmg_function:Callable[[nx.DiGraph, str], nx.DiGraph] = bmg, 
                top_n:int = 10,
                step_size:int = 1, 
                tree_likeness_function:Callable[[nx.DiGraph], int] = compute_tree_likeness, 
                mode:str="weak"):

    """
        Simplifies a network while keeping its bmg constant through a series of beam search steps. The top n networks get chosen to advance to the next step.
    """

    networks = [network]
    for _ in range(max_number_of_steps):
        networks = beam_search_step(networks, bmg_function, top_n, step_size, tree_likeness_function, mode)
    return(networks)

### GREEDY SEARCH

# When we can remove an edge while keeping the bmg this automatically improves the score so we do not need to check it explicitly
def remove_hybrid_edge(network, network_bmg, bmg_function, mode):
    nodes = list(network.nodes)
    random.shuffle(nodes)
    for child in nodes:
        parents = list(network.predecessors(child))
        if len(parents) < 2:
            continue

        random.shuffle(parents)
        for parent in parents:
            if network.out_degree(parent) <= 1:
                continue
            network.remove_edge(parent, child)
            new_bmg = bmg_function(network, mode)

            if nx.utils.graphs_equal(network_bmg, new_bmg):
                return network, True
            else:
                network.add_edge(parent, child)
    return network, False

def try_pulling_up(network, score, network_bmg, bmg_function, tree_likeness_function, mode):
    nodes = list(network.nodes)
    random.shuffle(nodes)
    for grandparent in nodes:
        grandparent_successors = list(network.successors(grandparent))
        for parent in grandparent_successors:
            if network.out_degree(parent) <= 1:
                continue
            parent_successors = list(network.successors(parent))
            for child in parent_successors:
                network.remove_edge(parent, child)
                network.add_edge(grandparent, child)

                new_score = extended_tree_likeness(network, network_bmg, bmg_function=bmg_function, tree_likeness_function=tree_likeness_function, mode= mode)
                if new_score > score:
                    remove_non_informative_nodes(network)
                    remove_redundant_vertices(network)
                    return network, new_score, True
                else:
                    network.remove_edge(grandparent, child)
                    network.add_edge(parent, child)

    return network, score, False

def try_pulling_down(network, score, network_bmg, bmg_function, tree_likeness_function, mode):
    nodes = list(network.nodes)
    random.shuffle(nodes)
    for parent in nodes:
        if network.out_degree(parent) <= 1:
            continue
        for child in network.successors(parent):
            for new_parent in network.successors(parent):
                if child == new_parent:
                    continue

                workingcopy = deepcopy(network)
                pull_down(workingcopy, child, parent, new_parent)
                remove_non_informative_nodes(workingcopy)
                remove_redundant_vertices(workingcopy)

                workingcopy_score = extended_tree_likeness(workingcopy, network_bmg, bmg_function=bmg_function, tree_likeness_function=tree_likeness_function, mode= mode)
                if workingcopy_score > score:
                    return workingcopy, workingcopy_score, True
    return network, score, False

def add_cherry_edge(network, network_bmg):
    for node in network.nodes:
        if network.out_degree(node) != 0:
            continue
        for target in network.nodes:
            if network.out_degree(target) != 0 or bool(set(network.predecessors(node)) & set(network.predecessors(target))):
                continue
            if network.nodes[target]["color"] != network.nodes[node]["color"]:
                continue
            for parent in network.predecessors(target):
                network.add_edge(parent, node)
                if not nx.utils.graphs_equal(network_bmg, bmg(network)):
                    network.remove_edge(parent, node)
                else:
                    print(f"added cherry edge {parent} - {node}")
                    return network, True
    return network, False

def greedy_search(network: nx.DiGraph,
                  max_number_of_steps:int = 100,
                  bmg_function:Callable[[nx.DiGraph, str], nx.DiGraph] = bmg,
                  tree_likeness_function:Callable[[nx.DiGraph], int] = compute_tree_likeness,
                  mode:str="weak"):
    network_bmg = bmg_function(network, mode)
    score = extended_tree_likeness(network, network_bmg, bmg_function, tree_likeness_function, mode="weak")

    for i in range(max_number_of_steps):
        print(f"simplifying step {i+1}/{max_number_of_steps}")

        #remove hybrid edges
        network, valid = remove_hybrid_edge(network, network_bmg, bmg_function, mode)
        if valid:
            continue

        #pull up action
        network, score, valid = try_pulling_up(network, score, network_bmg, bmg_function, tree_likeness_function, mode)
        if valid:
            continue

        #pull down action
        network, score, valid = try_pulling_down(network, score, network_bmg, bmg_function, tree_likeness_function, mode)
        if valid:
            continue

        network, valid = add_cherry_edge(network, network_bmg)

        if not valid:
            print("No further improvements found")
            return network

    return network