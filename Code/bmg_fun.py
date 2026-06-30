import networkx as nx
import matplotlib.colors as mcolors

def compute_bmg(T, sigma):
    """
    T:     a nx.DiGraph representing a rooted tree or network (edges parent→child)
    sigma: dict mapping each leaf to its color

    Returns: a nx.DiGraph representing the (weak) BMG
    """

    # Normalize sigma values to be hashable (convert arrays to tuples)
    sigma = {k: str(v)
             for k, v in sigma.items()}

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
                    if sigma[candidate] in remaining:  # best match found
                        colors_here.add(sigma[candidate])
                        BMG.add_edge(leaf, candidate)
                next_parents.extend(T.predecessors(parent))
            # remove all used up colors from remaining
            remaining -= colors_here
            parents = next_parents

    return BMG

def convert_to_nx(T) -> nx.DiGraph:
    """
    Converts an Asymmetree Tree into a NetworkX DiGraph.
    Instead of using the node ids (as the corresponding function does in the asymmetree package)
    it stores the node labels as the node names in the NetworkX DiGraph.
    """
    graph = nx.DiGraph()

    # not sure what this does in the original code, commenting it out for now
    #if not self.root:
    #    return graph, None

    for v in T.preorder():
        graph.add_node(v.label)
        for key, value in v.attributes():
            graph.nodes[v.label][key] = value

    for u, v, sibling_nr in T.edges_sibling_order():
        if u is v:
            raise RuntimeError(f"loop at {u} and {v}")
        graph.add_edge(u.label, v.label)
        graph.nodes[v.label]["sibling_nr"] = sibling_nr

    return graph