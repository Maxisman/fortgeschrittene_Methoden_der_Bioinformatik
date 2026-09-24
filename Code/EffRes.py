import numpy as np
import networkx as nx

def effective_resistance(U: nx.Graph, nodes: list) -> np.ndarray:
    """R[i,j] = effective resistance between nodes[i], nodes[j] (unit resistors on edges)."""
    L = nx.laplacian_matrix(U, nodelist=nodes).toarray().astype(float)
    Lp = np.linalg.pinv(L)
    d = np.diag(Lp)
    return d[:, None] + d[None, :] - 2 * Lp


def path_minus_resistance(G: nx.DiGraph, leaves_only: bool = False) -> float:
    """Tree-likeness score, higher = more tree-like, 0 iff G's underlying graph is a tree.

    -sum over pairs of (shortest path length - effective resistance).
    d == R exactly when there is a unique path; every cycle makes R < d.
    """
    U = G.to_undirected()
    nodes = list(U.nodes)
    R = effective_resistance(U, nodes)
    sp = dict(nx.all_pairs_shortest_path_length(U))
    idx = [i for i, v in enumerate(nodes) if (not leaves_only) or G.out_degree(v) == 0]
    return -sum(sp[nodes[i]][nodes[j]] - R[i, j]
                for a, i in enumerate(idx) for j in idx[a + 1:])