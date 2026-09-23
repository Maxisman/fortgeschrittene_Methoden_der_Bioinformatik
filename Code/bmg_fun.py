import networkx as nx
import numpy as np

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
        graph.add_node(str(v.label))
        for key, value in v.attributes():
            if key == "reconc":
                graph.nodes[str(v.label)]["color"] = value
            else:
                graph.nodes[str(v.label)][key] = value

    for u, v, sibling_nr in T.edges_sibling_order():
        if u is v:
            raise RuntimeError(f"loop at {u} and {v}")
        graph.add_edge(str(u.label), str(v.label))
        graph.nodes[str(v.label)]["sibling_nr"] = sibling_nr

    return graph


# --------------------------------------------------------------------------------------------------
#                                       Thinness classes for BMG
# --------------------------------------------------------------------------------------------------


import networkx as nx


def thinness_graph(G: nx.DiGraph, color_dict: dict | None = None):
    """Collapse the thinness classes of a colored digraph.

    Nodes with the same color, the same predecessors and the same successors
    are merged into one node. Singleton classes keep their original name;
    larger classes are named by their sorted member names joined with "-".
    The input graph is not modified. Nodes of the result carry only the
    'color' attribute, and edges carry no attributes.

    Args:
        G: A digraph whose nodes have the 'color' attribute.
        color_dict: Optional dict mapping every node of G to a color.

    Returns:
        The collapsed graph H if color_dict is None, otherwise a tuple
        (H, new_color_dict), where new_color_dict maps each class name to
        the color its members have in color_dict.
    """
    # 1) Group nodes by their signature (color, in-neighbors, out-neighbors).
    classes = {}
    for v in G.nodes:
        key = (
            G.nodes[v]["color"],
            frozenset(G.predecessors(v)),
            frozenset(G.successors(v)),
        )
        classes.setdefault(key, []).append(v)

    # 2) Create one node per class (local lookup only, not returned).
    H = nx.DiGraph()
    class_of = {}
    new_color_dict = {} if color_dict is not None else None
    for (color, _, _), members in classes.items():
        name = "-".join(sorted(members))
        H.add_node(name, color=color)
        for v in members:
            class_of[v] = name

        if color_dict is not None:
            first = color_dict[members[0]]
            for v in members[1:]:
                if not np.array_equal(color_dict[v], first):
                    raise ValueError(
                        f"members of class '{name}' have different colors in color_dict"
                    )
            new_color_dict[name] = first

    # Guard against name collisions, e.g. an original node already named "a1-a2".
    if H.number_of_nodes() != len(classes):
        raise ValueError("class names collide; check for '-' in node names")

    # 3) Map every original edge onto its classes; duplicates collapse automatically.
    H.add_edges_from((class_of[u], class_of[v]) for u, v in G.edges)

    if color_dict is None:
        return H
    return H, new_color_dict