import networkx as nx
from graph_functionality import lists_equal
import random

"""
    This script provides a collection of graph editing operations
"""

def pull_up (G:nx.DiGraph, child, parent, grandparent):
    """
    pulls up node child (which is a child of parent that itself is a child of grandparent) and attaches it to grandparent

    Parameters
    ----------
    G: nx.DiGraph
        Graph on which the operation is done
    child: name of a node
        node which should be reattached
    parent: name of node
        original parent of child which should be unattached
    grandparent: name of node
        parent of parent and node to which child should be reattached

    Returns
    -------
    G: nx.DiGraph
        input graph which is now edited to have the pull up operation executed
    """

    if not (child in list(G.successors(parent)) and parent in list(G.successors(grandparent))):
        raise ValueError("Parent not child of grandparent or child not child of parent")
    
    G.remove_edge(parent, child)
    G.add_edge(grandparent, child)

    return G

def pull_down (G:nx.DiGraph, child, parent, new_parent):
    """
    pulls down node child (which is a child of parent) to a node new_parent which must be a child of parent
    """
    # if asked to pull down to a leaf it pulls down to the edge instead
    if G.out_degree(new_parent) == 0:
        pull_down_edge(G, child, parent, new_parent)
        return
    
    if not (child in list(G.successors(parent)) and new_parent in list(G.successors(parent))):
        raise ValueError("Child not a child of parent or new_parent not a child of parent")

    G.remove_edge(parent, child)
    G.add_edge(new_parent, child)

    return G

def create_new_node_name(child, node_target):
    """
        Creates a new name for a parent of child and node_target. The name is parent_ followed by all leaves in lexicographical order seperated by underscore _
    """
    PARENT_IDENTIFIER = "p"

    child = str(child).split("_")
    if child[0] == PARENT_IDENTIFIER:
        child = child[1:]
    node_target = str(node_target).split("_")
    if node_target[0] == PARENT_IDENTIFIER:
        node_target = node_target[1:]
    leaves = child + node_target

    leaves.sort()

    new_node_name = PARENT_IDENTIFIER + "_" + "_".join(leaves)

    return new_node_name

def pull_down_edge(G:nx.DiGraph, child, node_origin, node_target):
    """
    pulls down node child (which is a child of node_origin) onto the edge node_origin -> node_target
    """
    if not (child in list(G.successors(node_origin)) and node_target in list(G.successors(node_origin))):
        raise ValueError("Child not a child of node_origin or node_target not a child of node_origin")
    
    if G.out_degree(node_origin) <= 2:
        return G
    
    new_node_name = create_new_node_name(child, node_target)

    G.add_node(new_node_name)
    G.remove_edge(node_origin, child)
    G.remove_edge(node_origin, node_target)
    G.add_edge(node_origin, new_node_name)
    G.add_edge(new_node_name, child)
    G.add_edge(new_node_name, node_target)

    return G

def remove_redundant_vertices(G:nx.DiGraph):
    """
    merges all vertices from G which have the same ancestors and children
    """
    removal = []
    for node in G.nodes():
        # do not remove leafes
        if G.out_degree(node) == 0:
            continue
        if node in removal:
            continue
        for node2 in G.nodes():
            if node2 == node:
                continue
            if lists_equal(list(G.successors(node)), list(G.successors(node2))):
                if lists_equal(list(G.predecessors(node)), list(G.predecessors(node2))):
                    removal.append(node2)
    for node in removal:
        G.remove_node(node)

    return G

def remove_hybrid_edge(G:nx.DiGraph, node, parent=None):
    """
    removes an edge of a hybrid node. When parent is not given a random edge is removed
    """
    if G.in_degree(node) <= 1:
        raise ValueError("Cannot remove edges from vertices with in-degree 0 or 1")
    
    if parent == None:
        parents = G.predecessors(node)
        parent = random.sample(parents, 1) #do we want randomness?
    
    G.remove_edge(parent, node)

    return G

def remove_non_informative_nodes(G:nx.DiGraph):
    """
        removes all nodes that have only one predecessor and successor to simplify a network
    """
    for node in list(G.nodes()):
        if G.in_degree(node) == 1 and G.out_degree(node) == 1:
            G.add_edge(list(G.predecessors(node))[0], list(G.successors(node))[0])
            G.remove_node(node)

    return G
    
"""
def remove_node(G:nx.DiGraph, node):
    G.remove_node(node)
"""