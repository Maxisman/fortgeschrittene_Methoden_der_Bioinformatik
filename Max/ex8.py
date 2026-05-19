import networkx as nx
import matplotlib.pyplot as plt

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

G = nx.DiGraph()
G.add_node("b1",color="b")
G.add_node("b2",color="b")
G.add_node("c1",color="r")
G.add_node("c2",color="r")
G.add_node("a1",color="g")
G.add_edges_from([("roh", "u"), ("u", "a1"), ("u", "w"), ("w", "b1"), ("w", "c1"), ("roh", "v"), ("v", "b2"), ("v", "c2")])
#nx.draw(G, with_labels=True)
#plt.show()

nx.draw(compute_bmg(G, "roh", {"a1" : "g", "b1":"b", "b2":"b", "c1":"r", "c2":"r"}), with_labels=True)
plt.show()
