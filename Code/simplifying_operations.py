import networkx as nx
from _collections_abc import Callable
import random
from bmg_Tony import bmg
from graph_functionality import compute_tree_likeness
from network_editing_operations import remove_non_informative_nodes, remove_redundant_vertices
import itertools

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
                            return network, new_score, True
                else:
                    if new_score > score:
                        if(nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg)):
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
        parent_successors = list(network.successors(parent))
        for child in parent_successors:
            for new_parent in parent_successors:
                if child == new_parent:
                    continue
                if network.out_degree(new_parent) == 0: # in this case pulling down would not make sense as it would remove a leaf #TODO: Is this right?
                    continue

                network.remove_edge(parent, child)
                network.add_edge(new_parent, child)

                new_score = tree_likeness_function(network)
                if allow_equal_score:
                    if new_score >= score:
                        if nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                            return network, new_score, True
                else:
                    if new_score > score:
                        if nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                            return network, new_score, True
                        
                network.add_edge(parent, child)
                network.remove_edge(new_parent, child)
    return network, score, False

def remove_diamond(network, network_bmg, bmg_mode):
    nodes = list(network.nodes)
    random.shuffle(nodes)
    for node in nodes:
        parents = list(network.predecessors(node))
        for parent1 in parents:
            for parent2 in parents:
                if parent1 == parent2:
                    continue
                lca = nx.lowest_common_ancestor(network, parent1, parent2)
                if lca == parent1 or lca == parent2:
                    continue
                network.remove_edge(parent1, node)
                network.remove_edge(parent2, node)
                network.add_edge(lca, node)
                if nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                    return network, True
                network.remove_edge(lca, node)
                network.add_edge(parent1, node)
                network.add_edge(parent2, node)
    return network, False

def combine_nodes(network, network_bmg, bmg_mode):
# Function from Tony, explanation missing
    changed = False
    inner_nodes = [node for node in network.nodes if network.out_degree(node) > 0 and network.in_degree(node) > 0]
    for node1, node2 in itertools.combinations(inner_nodes, 2):

        # Knoten könnte durch eine frühere, akzeptierte Änderung schon entfernt worden sein
        if not network.has_node(node1) or not network.has_node(node2):
            continue

        if (set(network.predecessors(node1)) == set(network.predecessors(node2))
                and network.out_degree(node1) > 0
                and network.out_degree(node2) > 0):

            #RBC2 = network.copy()  # echte, unabhängige Kopie

            predecessors = set(network.predecessors(node1))
            node1_successors = list(network.successors(node1))
            node2_successors = list(network.successors(node2))

            for successor in node1_successors:
                network.add_edge(node2, successor)
            network.remove_node(node1)

            if nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                changed = True
            else:
                current_node2_successors = list(network.successors(node2))
                for successor in current_node2_successors:
                    network.remove_edge(node2, successor)
                for successor in node2_successors:
                    network.add_edge(node2, successor)
                for predecessor in predecessors:
                    network.add_edge(predecessor, node1)
                for successor in node1_successors:
                    network.add_edge(node1, successor)
                if not nx.utils.graphs_equal(bmg(network, bmg_mode), network_bmg):
                    raise ValueError("Combine nodes in-place recovery is broken. Contact Max")
    return network, changed


def greedy_search(input_network: nx.DiGraph,
                  max_number_of_steps:int = 100,
                  tree_likeness_function:Callable[[nx.DiGraph], int] = compute_tree_likeness,
                  bmg_mode:str="weak", report_step_num:bool =False):
    """ Greedily searches for graph editing operations that can be performed on a network to make it more tree-like according to the tree_likeness_function.

        Parameters
        ----------
        input_network: nx.DiGraph
            network that will be edited to be more tree-like
        max_number_of_steps: int
            maximum number of editing steps before the final network is returned
        tree_likeness_function: Callable[[nx.DiGraph], int]
            function that measures the tree-likeness of a network numerically
        bmg_mode: String
            "weak" or "strong" depending on the best match type
        report_step_num: Boolean
            use True when you want to receive the number of steps as second output, also stops prints if true

        Returns
        -------
        network: nx.DiGraph
            more tree like version of the network with the same best match graph

    """
    network = input_network.copy()
    network_bmg = bmg(network, bmg_mode)
    score = tree_likeness_function(network)
    equal_score_steps = 0

    for i in range(max_number_of_steps):
        if not report_step_num:
            print(f"simplifying step {i+1}/{max_number_of_steps}")

        remove_non_informative_nodes(network)
        remove_redundant_vertices(network)
        score = tree_likeness_function(network)

        #contracting edges action
        # network, score, valid = contract_edge(network, score, network_bmg, tree_likeness_function, bmg_mode)
        # if valid:
        #     equal_score_steps = 0
        #     continue

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

        # #hybrid edge removal
        # network, valid = remove_hybrid_edge(network, network_bmg, bmg_mode)
        # if valid:
        #     equal_score_steps = 0
        #     score = score -1
        #     continue

        #removing diamonds
        #network, valid = remove_diamond(network, network_bmg, bmg_mode)
        #if valid:
        #    equal_score_steps = 0
        #    score = tree_likeness_function(network)
        #    continue

        if random.randint(0,1) == 0:
            network, score, valid = try_pulling_up(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=True)
            if not valid:
                network, score, valid = try_pulling_down(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=True)
        else:
            network, score, valid = try_pulling_down(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=True)
            if not valid:
                network, score, valid = try_pulling_up(network, score, network_bmg, tree_likeness_function, bmg_mode, allow_equal_score=True)

        equal_score_steps += 1

        if equal_score_steps > 10:
            network, valid = combine_nodes(network, network_bmg, bmg_mode)
            if valid:
                continue
            if report_step_num:
                return network, i
            else:
                print("No further improvements found")
            return network
    if report_step_num:
        return network, i
    return network