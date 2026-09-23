import itertools
import networkx as nx
from bmg_Tony import bmg

def informative_triples(G, color="color"):
    by_color = {}
    for v, c in G.nodes(data=color):
        by_color.setdefault(c, []).append(v)
    R = []
    for a, ca in G.nodes(data=color):
        for c, members in by_color.items():
            if c == ca:
                continue
            hits   = [b for b in members if G.has_edge(a, b)]
            misses = [b for b in members if not G.has_edge(a, b)]
            R.extend((a, b, b2) for b in hits for b2 in misses)
    return R

def _aho(R, L, T, counter):
    if len(L) == 1:
        return next(iter(L))
    aux = nx.Graph()
    aux.add_nodes_from(L)
    aux.add_edges_from((a, b) for a, b, _ in R)
    comps = list(nx.connected_components(aux))
    if len(comps) == 1:
        return None                      # inconsistent
    node = f"inner {next(counter)}"       # unique, can't clash with leaf names
    T.add_node(node)
    for C in comps:
        R_C = [t for t in R if t[0] in C and t[1] in C and t[2] in C]
        child = _aho(R_C, C, T, counter)
        if child is None:
            return None
        T.add_edge(node, child)
    return node


# --------------------------------------------------------------------------------------------------
#                                       LRT FROM BMG
# --------------------------------------------------------------------------------------------------


def lrt_from_bmg(G: nx.DiGraph, color="color") -> nx.DiGraph:
    T = nx.DiGraph()
    # add nodes from BMG
    T.add_nodes_from((v, {color: c}) for v, c in G.nodes(data=color))
    root = _aho(informative_triples(G, color), set(G.nodes), T, itertools.count())
    if root is None:
        return None                                   # R inconsistent
    if set(bmg(T).edges) != set(G.edges):
        return None                                   # not a BMG
    #T.graph["root"] = root
    return T