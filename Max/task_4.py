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
                path_length = len(nx.shortest_path(G, root, ancestor))
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

# network editing operations:

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
    pulls down node child (which is a child of parent to a node new_parent which must be a child of parent
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

def display_multiple_trees(graphs: list, sigma):
    fig, axes = plt.subplots(2, len(graphs), figsize=(4 * len(graphs), 10))
    for i, G in enumerate(graphs):
        pos = graphviz_layout(G, prog="dot")
        nx.draw(G, pos, ax=axes[0,i], with_labels=True)
        bmg = compute_bmg(G, "roh", sigma) #TODO: remove magic value "roh"
        nx.draw(bmg, nx.circular_layout(bmg), ax=axes[1,i], with_labels=True)
    plt.show()



#test code
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
print(G.edges)
pull_down(G, "w", "u", "c1")
print(graphs_equal(compute_bmg(original, "roh", sigma), compute_bmg(G, "roh", sigma)))
display_multiple_trees([original, G], sigma)