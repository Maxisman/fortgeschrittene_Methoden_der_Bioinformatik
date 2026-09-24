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

def compute_tree_likeness(G):
    """
    computes the tree likeness score as negative (number of edges - 2* number of nodes). The higher the score the more tree-like

    The idea behind that is that an ideal tree has as few edges as possible (especially no hybrid edges). However each node has at least two edges so we do not want to discourage creating more nodes (for now)
    """
    return -len(G.edges())

def color_dict_to_sequence(G:nx.digraph, node_to_color_dict:dict):
    if node_to_color_dict == None:
        return None
    sequence = []
    for node in G.nodes:
        if node in node_to_color_dict.keys():
            sequence.append(node_to_color_dict[node])
        else:
            sequence.append([0.5, 0.5, 0.5, 1.])
    return sequence

def display_multiple_trees(graphs: list, node_to_color_dict = None, tree_likeness_function = compute_tree_likeness):
    fig, axes = plt.subplots(2, max(len(graphs), 2), figsize=(4 * len(graphs), 10))
    bmg_pos = nx.circular_layout(bmg(graphs[0], "weak"))
    for i, G in enumerate(graphs):
        #graph
        pos = graphviz_layout(G, prog="dot")
        color_sequence = color_dict_to_sequence(G, node_to_color_dict)
        nx.draw(G, pos, node_color= color_sequence, ax=axes[0,i], with_labels=True)

        #bmg
        gbmg = bmg(G, "weak")
        node_color = color_dict_to_sequence(gbmg, node_to_color_dict)
        nx.draw(gbmg, bmg_pos, node_color= node_color, ax=axes[1,i], with_labels=True)

        #tree likeness score
        tree_likeness = tree_likeness_function(G)
        bbox = axes[1, i].get_position()
        x_center = (bbox.x0 + bbox.x1) / 2
        fig.text(x_center, bbox.y0 - 0.03, round(tree_likeness, 5), ha="center", fontsize=12)
    plt.show()