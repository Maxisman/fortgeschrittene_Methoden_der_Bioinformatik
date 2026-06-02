import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
from networkx.drawing.nx_pydot import graphviz_layout

def lca(T, root, x, y):
    path_x = nx.shortest_path(T, root, x)
    path_y = nx.shortest_path(T, root, y)

    # Walk both paths from the root.
    # As long as they agree, track the current vertex.
    # The last vertex where they agree is the lca.
    last = root
    for node in path_x:
        if node in path_y:
            last = node
        else:
            return last

def compute_bmg(T, root, sigma):
    """
    T:     a nx.DiGraph representing a rooted tree (edges parent→child)
    root:  the root vertex
    sigma: dict mapping each leaf to its color
    
    Returns: a nx.DiGraph representing the BMG
    """
    leaves = list(sigma.keys())
    all_colors = set(sigma.values())
    BMG = nx.DiGraph()
    for node, color in sigma.items():
        BMG.add_node(node, color=color)
    
    # For each leaf x, for each color s ≠ σ(x):
    #   1. Find all leaves y with σ(y) = s (the "candidates").
    #   2. Compute lca_depth(x, y) for each candidate.
    #      (lca_depth = distance from root to lca(x,y) — deeper = closer relative)
    #   3. Find the maximum depth among candidates.
    #   4. Add arc x→y for every candidate achieving that maximum.
    # YOUR CODE HERE (use your lca function from 0.4)

    for leaf in leaves:
        for color in all_colors:
            if sigma[leaf] == color:
                continue
            candidates = [key for key, value in sigma.items() if value == color]
            
            candidate_dict = {}
            for candidate in candidates:
                ancestor = lca(T, root, leaf, candidate)
                path_length = len(nx.shortest_path(T, root, ancestor))
                candidate_dict.update({candidate:path_length})

            best_matches = [key for key,value in candidate_dict.items() if value == max(candidate_dict.values())]
            
            BMG.add_edges_from([(leaf, best_match) for best_match in best_matches])

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
    fig, axes = plt.subplots(2, len(graphs), figsize=(4 * len(graphs), 10))
    for i, G in enumerate(graphs):
        pos = graphviz_layout(G, prog="dot")
        nx.draw(G, pos, ax=axes[0,i], with_labels=True)
        bmg = compute_bmg(G, "roh", sigma) #TODO: remove magic value "roh"
        nx.draw(bmg, nx.circular_layout(bmg), ax=axes[1,i], with_labels=True)
    plt.show()