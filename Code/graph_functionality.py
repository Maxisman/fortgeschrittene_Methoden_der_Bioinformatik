import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from bmg_Tony import bmg
#import simplifying_operations

def lists_equal(l1:list, l2:list):
    l1.sort()
    l2.sort()
    try:
        return all(x == y for x, y in zip(l1, l2, strict=True))
    except ValueError:
        return False

def graphs_equal (G1:nx.DiGraph, G2: nx.DiGraph): #TODO: check whether nodes and edges have same count
    """
    checks whether nx.DiGraphs equal one another under the condition that the nodes are named equally
    """
    try:
        for node in G1.nodes():
            if not lists_equal(list(G1.successors(node)), list(G2.successors(node))):
                return False
    except nx.NetworkXError:
        return False
    
    if len(list(G1.nodes())) != len(list(G2.nodes())):
        return False
    
    return True

def compute_tree_likeness(G):
    """
    computes the tree likeness score as negative (number of edges - 2* number of nodes). The higher the score the more tree-like

    The idea behind that is that an ideal tree has as few edges as possible (especially no hybrid edges). However each node has at least two edges so we do not want to discourage creating more nodes (for now)
    """
    return -( len(G.edges()) - 1.9 * len(G.nodes())) #2 we need to see which scalar should value many nodes. Too many nodes are just making the graph more complicated unneccessarily

def helper_tree_likeness(G, bmg, bmg_function=bmg, tree_likeness_function=compute_tree_likeness, NEGATIVE_INFINITY = -1000000, mode="weak"):
    """
    Helper for beam_search_step(). Returns a score of tree likeness or NEGATIVE_INFINITY if the network's bmg is wrong
    """
    if not graphs_equal(bmg, bmg_function(G, mode)):
        return (NEGATIVE_INFINITY)
    else:
        return (tree_likeness_function(G))

def display_multiple_trees(graphs: list):
    fig, axes = plt.subplots(2, max(len(graphs), 2), figsize=(4 * len(graphs), 10))
    for i, G in enumerate(graphs):
        pos = graphviz_layout(G, prog="dot")
        nx.draw(G, pos, ax=axes[0,i], with_labels=True)
        gbmg = bmg(G)
        nx.draw(gbmg, nx.circular_layout(gbmg), ax=axes[1,i], with_labels=True)

        tree_likeness = helper_tree_likeness(G,gbmg)
        bbox = axes[1, i].get_position()
        x_center = (bbox.x0 + bbox.x1) / 2
        fig.text(x_center, bbox.y0 - 0.03, round(tree_likeness, 5), ha="center", fontsize=12)
    plt.show()