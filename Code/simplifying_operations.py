from network_editing_operations import * #TODO: remove eventually
from copy import deepcopy #TODO: remove eventually
import networkx as nx
from _collections_abc import Callable
from bmg_Tony import bmg
from graph_functionality import compute_tree_likeness

"""
    This script provides methods to simplify a graph network
"""

def remove_hybrid_edge(network, network_bmg, bmg_mode):
    """ DEPRECATED Removes the first hybrid edge from a graph that can be removed while keeping the best match graph unchanged. Note that we do not consider the tree likeness score here as it is assumed that getting rid of hybrid edges always improves tree likeness.
    
        Parameters
        ----------
        network: nx.Digraph
            Graph from which a hybrid edge should be removed
        network_bmg: nx.DiGraph
            best match graph of network that should be kept intact
        bmg_mode: String
            "weak" or "strong", type of best matches that should be assessed
    
        Returns
        -------
        network: nx.DiGraph
            network with a hybrid edge removed or the same network if no such removal is possible
        valid: bool
            True if a hybrid was successfully removed and False if this was not possible
    """

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

            if nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                return network, True
            else:
                network.add_edge(parent, child)
    return network, False

def contract_edge(network, score, network_bmg, tree_likeness_function, bmg_mode):
    """ Contracts a random edge in the network keeping the bmg intact if this is possible. A contraction takes an edge (u->v), attaches v's children to u and deletes v
    
        Parameters
        ----------
        network: nx.Digraph
            Graph from which an edge should be contracted
        score:
            tree_likeness score of the original network
        network_bmg: nx.DiGraph
            best match graph of network that should be kept intact
        tree_likeness_function:
            function used to evaluate tree likeness
        bmg_mode: String
            "weak" or "strong", type of best matches that should be assessed
    
        Returns
        -------
        network: nx.DiGraph
            network with an edge contracted or the same network if no such contraction is possible
        score: int
            new tree likeness score of the network
        valid: bool
            True if an edge was successfully contracted and False if this was not possible
    """

    nodes = list(network.nodes)
    random.shuffle(nodes)
    for parent in nodes:
        children = list(network.successors(parent))
        for child in children:
            if network.out_degree(child) == 0:
                continue

            grandchildren = list(network.successors(child))
            for grandchild in grandchildren:
                network.add_edge(parent, grandchild)
            network.remove_node(child)
            newscore = tree_likeness_function(network)

            if newscore > score:
                if nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                    return network, newscore, True
                
            network.add_node(child)
            for grandchild in grandchildren:
                network.add_edge(child, grandchild)
                network.remove_edge(parent, grandchild)
            network.add_edge(parent, child)
    return network, score, False

def try_pulling_up(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score):
    """ Uses the "pull up" operation on a random set of nodes if this is possible while keeping the network's bmg intact
    
        Parameters
        ----------
        network: nx.Digraph
            Graph on which a "pull up" action should be performed
        score:
            tree_likeness score of the original network
        network_bmg: nx.DiGraph
            best match graph of network that should be kept intact
        tree_likeness_function:
            function used to evaluate tree likeness
        bmg_mode: String
            "weak" or "strong", type of best matches that should be assessed
        allow_equal_score: bool
            switch whether changes that keep the score the same should be accepted
    
        Returns
        -------
        network: nx.DiGraph
            network with a completed "pull up" operation or the same network if no such operation is possible
        score: int
            new tree likeness score of the network
        valid: bool
            True if any "pull up" operation was successful and False if none was possible
    """
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

                new_score = tree_likeness_function(network)
                if allow_equal_score:
                    if new_score >= score:
                        if(nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg)):
                            remove_non_informative_nodes(network)
                            remove_redundant_vertices(network)
                            return network, new_score, True
                else:
                    if new_score > score:
                        if(nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg)):
                            remove_non_informative_nodes(network)
                            remove_redundant_vertices(network)
                            return network, new_score, True
                    
                network.remove_edge(grandparent, child)
                network.add_edge(parent, child)

    return network, score, False

def try_pulling_down(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score):
    """ Uses the "pull down" operation on a random set of nodes if this is possible while keeping the network's bmg intact
    
        Parameters
        ----------
        network: nx.Digraph
            Graph on which a "pull down" action should be performed
        score:
            tree_likeness score of the original network
        network_bmg: nx.DiGraph
            best match graph of network that should be kept intact
        tree_likeness_function:
            function used to evaluate tree likeness
        bmg_mode: String
            "weak" or "strong", type of best matches that should be assessed
        allow_equal_score: bool
            switch whether changes that keep the score the same should be accepted
    
        Returns
        -------
        network: nx.DiGraph
            network with a completed "pull down" operation or the same network if no such operation is possible
        score: int
            new tree likeness score of the network
        valid: bool
            True if any "pull down" operation was successful and False if none was possible
    """
    nodes = list(network.nodes)
    random.shuffle(nodes)
    for parent in nodes:
        if network.out_degree(parent) <= 1:
            continue
        for child in network.successors(parent):
            for new_parent in network.successors(parent):
                if child == new_parent:
                    continue

                workingcopy = deepcopy(network) #TODO: remove need for deepcopy
                pull_down(workingcopy, child, parent, new_parent)
                remove_non_informative_nodes(workingcopy)
                remove_redundant_vertices(workingcopy)

                workingcopy_score = tree_likeness_function(workingcopy)
                if allow_equal_score:
                    if workingcopy_score >= score:
                        if nx.utils.graphs_equal(bmg(workingcopy, bmg_mode), network_bmg):
                            return workingcopy, workingcopy_score, True
                else:
                    if workingcopy_score > score:
                        if nx.utils.graphs_equal(bmg(workingcopy, bmg_mode), network_bmg):
                            return workingcopy, workingcopy_score, True
    return network, score, False

def greedy_search(network: nx.DiGraph,
                  max_number_of_steps:int = 100,
                  tree_likeness_function:Callable[[nx.DiGraph], int] = compute_tree_likeness,
                  bmg_mode:str="weak"):
    """ Greedily searches for graph editing operations that can be performed on a network to make it more tree-like according to the tree_likeness_function.

        Parameters
        ----------
        network: nx.DiGraph
            network that will be edited to be more tree-like
        max_number_of_steps: int
            maximum number of editing steps before the final network is returned
        tree_likeness_function: Callable[[nx.DiGraph], int]
            function that measures the tree-likeness of a network numerically
        bmg_mode: String
            "weak" or "strong" depending on the best match type

        Returns
        -------
        network: nx.DiGraph
            more tree like version of the network with the same best match graph

    """
    network_bmg = bmg(network, bmg_mode)
    score = tree_likeness_function(network)
    equal_score_steps = 0

    for i in range(max_number_of_steps):
        print(f"simplifying step {i+1}/{max_number_of_steps}")

        #contracting edges action
        network, score, valid = contract_edge(network, score, network_bmg, tree_likeness_function, bmg_mode)
        if valid:
            equal_score_steps = 0
            continue

        #pull up action
        network, score, valid = try_pulling_up(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=False)
        if valid:
            equal_score_steps = 0
            continue

        #pull down action
        network, score, valid = try_pulling_down(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=False)
        if valid:
            equal_score_steps = 0
            continue

        network, score, valid = try_pulling_up(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=True)
        network, score, valid = try_pulling_down(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=True)
        equal_score_steps += 1

        if equal_score_steps > 10:
            print("No further improvements found")
            return network

    return network