import networkx as nx
from collections import Counter

def BICcherry(G: nx.DiGraph) -> nx.DiGraph:
    # assert colored digraph
    assert isinstance(G, nx.DiGraph)
    assert all("color" in  G.nodes[v] for v in G.nodes)

    # assert properly colored (no edges between same color)
    colors = nx.get_node_attributes(G,"color")
    for u,v in G.edges():
        assert colors[u] != colors[v]

    # assert sicor in hub
    ## find all sicors
    color_counts = Counter(colors.values())
    sicor = [v for v,c in colors.items() if color_counts[c]==1]
    ## assert in-hub-ness
    for s in sicor:
        for u in G.nodes():
            if colors[u] != colors[s]:
                assert G.has_edge(u,s)

    # BICcherry



    # return
    return nx.DiGraph()

