import networkx as nx
from collections import Counter
import random
rng = random.Random(42)

def BICcherry(G: nx.DiGraph) -> nx.DiGraph:
    # ASSERTIONS
    ## assert colored digraph
    assert isinstance(G, nx.DiGraph)
    assert all("color" in G.nodes[v] for v in G.nodes)

    ## assert properly colored (no edges between same color)
    colors = nx.get_node_attributes(G,"color")
    for u,v in G.edges():
        assert colors[u] != colors[v]

    ## assert sicor in hub
    ### find all sicors
    color_counts = Counter(colors.values())
    sicor = [v for v,c in colors.items() if color_counts[c]==1]
    ### assert in-hub-ness
    for s in sicor:
        for u in G.nodes():
            if colors[u] != colors[s]:
                assert G.has_edge(u,s)

    # BIC-CHERRY
    ## initialize and root network digraph
    N = nx.DiGraph()
    N.add_node("rho")

    ## extract differently colored leafs from G
    cherrylist = []
    for key1, value1 in colors.items():
        for key2, value2 in colors.items():
            if key1 < key2 and value1 != value2:
                cherrylist.append(frozenset({str(key1), str(key2)}))
    ## add leaves and parent nodes to get uglycherry
    p_nodes = dict()
    for pair in cherrylist:
        x,y = sorted(pair)
        p_name = f"p_{x}_{y}"
        p_nodes[pair] = p_name
        N.add_edge("rho",p_name)
        N.add_edge(p_name, x)
        N.add_edge(p_name, y)
    ## add back color property to nodes
    for node, color in colors.items():
        N.nodes[str(node)]["color"] = color

    # EXTENSION
    ## find all cherrys x,y in N that don't have an edge x,y or y,x in G
    ### find *any* (optimize here? random for now) another x' or y' that has an edge in G
    ### introduce q_xy' or q_yx' below the corresponding p_xy or p_yx
    for pair, p_name in p_nodes.items():
        x,y = sorted(pair)
        if not G.has_edge(x,y):
            y_prime = rng.choice([str(v) for v in G.nodes() if v != y and colors[int(v)]==colors[int(y)]])
            ## insert q_xy' below p_xy
            q_name = f"q_{x}_{y}_{y_prime}"
            N.add_edge(p_name,q_name)
            N.add_edge(q_name, x)
            N.add_edge(q_name, y_prime)
        if not G.has_edge(y,x):
            x_prime = rng.choice([str(v) for v in G.nodes() if v != x and colors[int(v)]==colors[int(x)]])
            ## insert q_yx'' below p_xy
            q_name = f"q_{y}_{x}_{x_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, y)
            N.add_edge(q_name, x_prime)

    # return network
    return N


