import networkx as nx
from graph_functionality import *
import random
from copy import deepcopy


def pull_up (G:nx.DiGraph, child, parent, grandparent):
    """
    pulls up node child (which is a child of parent that itself is a child of grandparent) and attaches it to grandparent
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
    # if asked to pull down to a leave it pulls down to the edge instead
    if G.out_degree(new_parent) == 0:
        pull_down_edge(G, child, parent, new_parent)
        return
    
    if not (child in list(G.successors(parent)) and new_parent in list(G.successors(parent))):
        raise ValueError("Child not a child of parent or new_parent not a child of parent")

    G.remove_edge(parent, child)
    G.add_edge(new_parent, child)

    return G

def pull_down_edge(G:nx.DiGraph, child, node_origin, node_target):
    """
    pulls down node child (which is a child of node_origin) to the edge node_origin - node_target
    """
    if not (child in list(G.successors(node_origin)) and node_target in list(G.successors(node_origin))):
        raise ValueError("Child not a child of node_origin or node_target not a child of node_origin")
    
    new_node_name = "p_" + str(child) + "_" + str(node_target)
    G.add_node(new_node_name)
    G.remove_edge(node_origin, child)
    G.remove_edge(node_origin, node_target)
    G.add_edge(node_origin, new_node_name)
    G.add_edge(new_node_name, child)
    G.add_edge(new_node_name, node_target)

def remove_redundant_vertices(G:nx.DiGraph): #make function more robust
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
    
def remove_node(G:nx.DiGraph, node):
    G.remove_node(node)



#test code
if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node("b1",color="b")
    G.add_node("b2",color="b")
    G.add_node("c1",color="r")
    G.add_node("c2",color="r")
    G.add_node("a1",color="g")
    G.add_edges_from([("roh", "u"), ("u", "a1"), ("u", "w"), ("w", "b1"), ("w", "c1"), ("roh", "v"), ("v", "b2"), ("v", "c2"), ("u", "c1")])
    sigma = {"a1" : "g", "b1":"b", "b2":"b", "c1":"r", "c2":"r"}
    #redundant nodes x and y
    G.add_edges_from([("roh", "x"), ("x", "b2"), ("x", "c2")])
    G.add_edges_from([("roh", "y"), ("y", "b2"), ("y", "c2")])
    original = G

    # basic operations
    # G = deepcopy(original)
    # pull_down(G, "a1", "u", "w")
    # H = deepcopy(original)
    # pull_up(H, "b1", "w", "u")
    # I = deepcopy(original)
    # remove_redundant_vertices(I)
    # print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(G, "roh", sigma)))
    # display_multiple_trees([original,H, G, I], sigma)

    # reach tree
    # G = deepcopy(original)
    # remove_redundant_vertices(G)
    # H = deepcopy(G)
    # pull_down(H, "c1", "u", "w")
    # print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(H, "roh", sigma)))
    # display_multiple_trees([original, G, H], sigma)

    # break bmg
    G = deepcopy(original)
    pull_up(G, "a1", "u", "roh")
    #pull_down(G, "w", "u", "c1")
    print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(G, "roh", sigma)))
    display_multiple_trees([original, G], sigma)