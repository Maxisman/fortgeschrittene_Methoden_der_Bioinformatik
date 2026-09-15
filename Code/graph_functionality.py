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

def compute_tree_likeness(G):
    """
    computes the tree likeness score as negative (number of edges - 2* number of nodes). The higher the score the more tree-like

    The idea behind that is that an ideal tree has as few edges as possible (especially no hybrid edges). However each node has at least two edges so we do not want to discourage creating more nodes (for now)
    """
    return -( len(G.edges()) - 1 * len(G.nodes())) #2 we need to see which scalar should value many nodes. Too many nodes are just making the graph more complicated unneccessarily

def extended_tree_likeness(G, bmg, bmg_function=bmg, tree_likeness_function=compute_tree_likeness, NEGATIVE_INFINITY = -1000000, mode="weak"):
    """
    Returns a score of tree likeness or NEGATIVE_INFINITY if the network's bmg is wrong
    """
    if not nx.utils.graphs_equal(bmg, bmg_function(G, mode)):
        return (NEGATIVE_INFINITY)
    else:
        return (tree_likeness_function(G))

def display_multiple_trees(graphs: list):
    fig, axes = plt.subplots(2, max(len(graphs), 2), figsize=(4 * len(graphs), 10))
    bmg_pos = nx.circular_layout(bmg(graphs[0], "weak"))
    for i, G in enumerate(graphs):
        pos = graphviz_layout(G, prog="dot")
        nx.draw(G, pos, ax=axes[0,i], with_labels=True)
        gbmg = bmg(G)
        nx.draw(gbmg, bmg_pos, ax=axes[1,i], with_labels=True)

        tree_likeness = extended_tree_likeness(G,gbmg)
        bbox = axes[1, i].get_position()
        x_center = (bbox.x0 + bbox.x1) / 2
        fig.text(x_center, bbox.y0 - 0.03, round(tree_likeness, 5), ha="center", fontsize=12)
    plt.show()