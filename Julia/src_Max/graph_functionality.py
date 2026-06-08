import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
from networkx.drawing.nx_pydot import graphviz_layout


def compute_bmg(T, sigma):
    """
    T:     a nx.DiGraph representing a rooted tree (edges parent→child)
    root:  the root vertex
    sigma: dict mapping each leaf to its color
    
    Returns: a nx.DiGraph representing the BMG
    """
    leaves = list(sigma.keys())
    all_colors = set(sigma.values())
    BMG = nx.DiGraph()

    # first, add all leaves to the BMG
    for node, color in sigma.items():
        BMG.add_node(node, color=color)

    # second, add edges to nodes for best matches
    # loop through all leaves
    for leaf in leaves:
        remaining = all_colors - {sigma[leaf]}  # colors to which no best match has yet been found
        # access immediate predecessors
        parents = list(T.predecessors(leaf))

        # as long as parent(s) and colors still exist
        while remaining and parents:
            next_parents = []
            for parent in parents:
                # find all leaf descendants of this parent
                candidates = {n for n in nx.descendants(T, parent) if n in set(leaves)}
                # remove current leaf from candidates
                candidates -= {leaf}
                colors_here = set()
                # loop through candidates
                for candidate in candidates:
                    if sigma[candidate] in remaining: # best match found
                        colors_here.add(sigma[candidate])
                        BMG.add_edge(leaf, candidate)
                next_parents.extend(T.predecessors(parent))
            # remove all used up colors from remaining
            remaining -= colors_here
            parents = next_parents


    return BMG

def extract_informative_triples(BMG, sigma):
    """
    Returns a list of tuples (a, b, b_prime) meaning "ab|b'"
    """
    triples = []
    nodes = BMG.nodes()
    for a in nodes:
        successors = list(BMG.successors(a))
        for b in successors:
            for b_prime in nodes:
                if sigma[b] == sigma[b_prime] and not b_prime in successors:
                    triples.append((a,b,b_prime))
    return triples

def lists_equal(l1, l2):
    try:
        return all(x == y for x, y in zip(l1, l2, strict=True))
    except ValueError:
        return False

def graphs_equal (G1:nx.DiGraph, G2: nx.DiGraph):
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

def display_multiple_trees(graphs: list, sigma):
    fig, axes = plt.subplots(2, 1, figsize=(4 * len(graphs), 10))
    for i, G in enumerate(graphs):
        pos = graphviz_layout(G, prog="dot")
        nx.draw(G, pos, ax=axes[0], with_labels=True)
        bmg = compute_bmg(G, sigma)
        nx.draw(bmg, nx.circular_layout(bmg), ax=axes[1], with_labels=True)
    plt.show()