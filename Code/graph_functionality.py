import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from bmg_Tony import bmg

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

def display_multiple_trees(graphs: list):
    fig, axes = plt.subplots(2, len(graphs), figsize=(2 * len(graphs), 10))
    for i, G in enumerate(graphs):
        pos = graphviz_layout(G, prog="dot")
        nx.draw(G, pos, ax=axes[0,i], with_labels=True)
        gbmg = bmg(G)
        nx.draw(gbmg, nx.circular_layout(bmg), ax=axes[1,i], with_labels=True)
    plt.show()